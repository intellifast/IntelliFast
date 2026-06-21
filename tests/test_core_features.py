import io
import json
import sqlite3
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

import app as application
from werkzeug.security import generate_password_hash


class CoreFeatureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        application.DB_PATH = root / "test.db"
        application.UPLOAD_DIR = root / "uploads"
        application.BACKUP_DIR = root / "backups"
        application.app.config.update(TESTING=True, SECRET_KEY="test-secret", SERVER_NAME="localhost")
        application.init_db()
        conn = sqlite3.connect(application.DB_PATH)
        conn.execute("""INSERT INTO users(email,password_hash,full_name,display_name,email_verified,onboarded,timezone)
                        VALUES(?,?,?,?,1,1,'UTC')""",
                     ("member@example.com", generate_password_hash("StrongPass1"), "Member User", "Member"))
        conn.commit(); conn.close()
        self.client = application.app.test_client()
        self.client.get("/login")
        self.token = self._csrf()
        self.client.post("/login", data={"email":"member@example.com", "password":"StrongPass1", "csrf_token":self.token})
        self.token = self._csrf()

    def tearDown(self):
        self.temp.cleanup()

    def _csrf(self):
        with self.client.session_transaction() as session:
            return session["csrf_token"]

    def post(self, path, data=None, **kwargs):
        payload = dict(data or {}); payload.setdefault("csrf_token", self._csrf())
        return self.client.post(path, data=payload, **kwargs)

    def db_row(self, sql, args=()):
        conn = sqlite3.connect(application.DB_PATH); conn.row_factory = sqlite3.Row
        row = conn.execute(sql, args).fetchone(); conn.close(); return row

    def test_timer_schedule_pause_target_and_confirmed_early_completion(self):
        future = (application.user_now({"timezone":"UTC"}) + timedelta(hours=2)).isoformat(timespec="minutes")
        response = self.post("/fast/start", {"plan":"16:8", "hours":"2", "started_at":future})
        self.assertEqual(response.status_code, 200)
        fast_id = response.get_json()["id"]
        self.assertEqual(self.db_row("SELECT status FROM fasts WHERE id=?", (fast_id,))["status"], "scheduled")
        self.assertEqual(self.post(f"/fast/{fast_id}/action", {"action":"start_now"}).status_code, 200)
        blocked = self.post(f"/fast/{fast_id}/action", {"action":"complete", "mood":"Good"})
        self.assertEqual(blocked.status_code, 409)
        done = self.post(f"/fast/{fast_id}/action", {"action":"complete", "confirm_early":"1", "mood":"Good", "mood_note":"Steady"})
        self.assertEqual(done.status_code, 200)
        row = self.db_row("SELECT status,completed_early,mood,mood_note FROM fasts WHERE id=?", (fast_id,))
        self.assertEqual((row["status"], row["completed_early"], row["mood"]), ("completed", 1, "Good"))

    def test_target_reached_event_is_idempotent(self):
        start = (application.user_now({"timezone":"UTC"}) - timedelta(hours=2)).isoformat()
        conn = sqlite3.connect(application.DB_PATH)
        uid = conn.execute("SELECT id FROM users").fetchone()[0]
        cur = conn.execute("INSERT INTO fasts(user_id,started_at,target_hours,plan,status) VALUES(?,?,?,?,?)", (uid,start,1,"Custom","active"))
        conn.commit(); conn.close()
        self.client.get("/api/timer/status"); self.client.get("/api/timer/status")
        row = self.db_row("SELECT target_reached_at FROM fasts WHERE id=?", (cur.lastrowid,))
        count = self.db_row("SELECT COUNT(*) AS n FROM notifications WHERE title='Fasting target reached'")["n"]
        self.assertTrue(row["target_reached_at"]); self.assertEqual(count, 1)

    def test_due_reminder_delivers_once_and_can_be_edited_deleted(self):
        now = application.user_now({"timezone":"UTC"})
        day = now.strftime("%a")
        response = self.post("/reminders", {"kind":"Hydration", "time":now.strftime("%H:%M"), "days":day,
                                             "channel":"both", "message":"Drink some water"})
        self.assertEqual(response.status_code, 302)
        reminder = self.db_row("SELECT * FROM reminders")
        with application.app.test_request_context("/"):
            application.g.user = application.db().execute("SELECT * FROM users").fetchone()
            with patch.object(application, "send_transactional_email") as sender:
                self.assertEqual(application.dispatch_due_reminders(send_email=True), 1)
                self.assertEqual(application.dispatch_due_reminders(send_email=True), 0)
                sender.assert_called_once()
        edited = self.post(f"/reminders/{reminder['id']}/edit", {"kind":"Daily check-in", "time":now.strftime("%H:%M"),
                           "days":day, "channel":"in_app", "message":"Check in"})
        self.assertEqual(edited.status_code, 302)
        self.assertEqual(self.db_row("SELECT kind FROM reminders WHERE id=?",(reminder["id"],))["kind"], "Daily check-in")
        self.post(f"/reminders/{reminder['id']}/delete")
        self.assertIsNone(self.db_row("SELECT id FROM reminders WHERE id=?",(reminder["id"],)))

    def test_history_pagination_filters_calendar_and_csv_preview_commit(self):
        conn = sqlite3.connect(application.DB_PATH)
        uid = conn.execute("SELECT id FROM users").fetchone()[0]
        now = application.user_now({"timezone":"UTC"})
        for index in range(12):
            start = now - timedelta(days=index+1, hours=14); end = start + timedelta(hours=14)
            conn.execute("INSERT INTO fasts(user_id,started_at,ended_at,target_hours,plan,status,notes) VALUES(?,?,?,?,?,'completed',?)",
                         (uid,start.isoformat(),end.isoformat(),14,"14:10",f"record {index}"))
        conn.commit(); conn.close()
        page = self.client.get("/history?page=2&min_hours=13&max_hours=15")
        self.assertEqual(page.status_code, 200); self.assertIn(b"Page 2 of 2", page.data)
        csv_data = "Start,End,Plan,Target hours,Status,Notes\n2030-01-01T20:00,2030-01-02T10:00,14:10,14,completed,Imported\n"
        preview = self.post("/history/import-preview", {"csv_file":(io.BytesIO(csv_data.encode()),"history.csv")}, content_type="multipart/form-data")
        self.assertEqual(preview.status_code, 302)
        token = self.db_row("SELECT token FROM import_previews")["token"]
        record = self.db_row("SELECT rows_json FROM import_previews WHERE token=?",(token,))
        imported = json.loads(record["rows_json"])[0]
        response = self.post(f"/history/import-commit/{token}", {"include_0":"1", "start_0":imported["start"], "end_0":imported["end"],
                             "plan_0":"14:10", "target_0":"14", "status_0":"completed", "notes_0":"Imported"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.db_row("SELECT COUNT(*) AS n FROM fasts WHERE notes='Imported'")["n"], 1)

    def test_ai_monthly_quota_counts_successes_and_admin_can_allocate(self):
        with patch.object(application, "gemini_reply", side_effect=RuntimeError("Provider unavailable")):
            failed = self.client.post("/api/ai-buddy", json={"message":"Will this count?"}, headers={"X-CSRF-Token":self._csrf()})
            self.assertEqual(failed.status_code, 503)
            self.assertEqual(self.db_row("SELECT COUNT(*) AS n FROM ai_usage WHERE status='success'")["n"], 0)
        with patch.object(application, "gemini_reply", return_value="A short supportive reply."):
            for index in range(5):
                response = self.client.post("/api/ai-buddy", json={"message":f"Message {index}"}, headers={"X-CSRF-Token":self._csrf()})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json()["quota"]["remaining"], 4-index)
            limited = self.client.post("/api/ai-buddy", json={"message":"One more"}, headers={"X-CSRF-Token":self._csrf()})
            self.assertEqual(limited.status_code, 429)
        conn = sqlite3.connect(application.DB_PATH)
        uid = conn.execute("SELECT id FROM users").fetchone()[0]
        conn.execute("UPDATE users SET is_admin=1 WHERE id=?",(uid,)); conn.commit(); conn.close()
        set_limit = self.post(f"/admin/users/{uid}/ai-quota", {"action":"set_limit", "amount":["8","3"]})
        self.assertEqual(set_limit.status_code, 302)
        grant = self.post(f"/admin/users/{uid}/ai-quota", {"action":"grant_extra", "amount":["8","3"], "note":"Testing"})
        self.assertEqual(grant.status_code, 302)
        with application.app.test_request_context("/"):
            application.g.user = application.db().execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone()
            quota = application.ai_quota(uid, application.g.user)
            self.assertEqual((quota["allowance"],quota["used"],quota["remaining"]),(11,5,6))


if __name__ == "__main__":
    unittest.main()
