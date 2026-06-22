import io
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app as application
from werkzeug.security import generate_password_hash


class ProductionFoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        application.DB_PATH = root / "test.db"
        application.UPLOAD_DIR = root / "uploads"
        application.BACKUP_DIR = root / "backups"
        application.app.config.update(TESTING=True, SECRET_KEY="test-secret", SERVER_NAME="localhost")
        application.init_db()
        self.client = application.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path="/login"):
        self.client.get(path)
        with self.client.session_transaction() as session:
            return session["csrf_token"]

    def create_user(self, email="admin@example.com", admin=False):
        conn = sqlite3.connect(application.DB_PATH)
        cur = conn.execute("""INSERT INTO users(email,password_hash,full_name,display_name,email_verified,onboarded,is_admin)
                            VALUES(?,?,?,?,1,1,?)""",
                           (email, generate_password_hash("StrongPass1"), "Admin User", "Admin", int(admin)))
        conn.commit(); conn.close(); return cur.lastrowid

    def login(self, email="admin@example.com"):
        token = self.csrf()
        response = self.client.post("/login", data={"email": email, "password": "StrongPass1", "csrf_token": token})
        self.assertEqual(response.status_code, 302)
        return self.csrf("/dashboard")

    def test_verified_registration_and_onboarding(self):
        token = self.csrf("/register")
        with patch.object(application, "send_transactional_email") as sender:
            response = self.client.post("/register", data={"full_name":"New User","email":"new@example.com",
                "password":"SecurePass1","accept_terms":"yes","csrf_token":token})
            self.assertEqual(response.status_code, 200)
            otp = sender.call_args.kwargs["otp_code"]
        token = self.csrf("/login")
        self.assertEqual(self.client.post("/verify-email", data={"email":"new@example.com","otp":otp,"csrf_token":token}).status_code, 302)
        token = self.csrf("/onboarding")
        response = self.client.post("/onboarding", data={"goal":"General wellness","experience":"Beginner","plan":"16:8",
            "start_time":"20:00","reminder_time":"19:45","timezone":"Asia/Calcutta","csrf_token":token})
        self.assertEqual(response.status_code, 302)

    def test_verification_otp_rejects_wrong_code_and_resend_replaces_it(self):
        token = self.csrf("/register")
        with patch.object(application, "send_transactional_email") as sender:
            self.client.post("/register", data={"full_name":"New User","email":"new@example.com",
                "password":"SecurePass1","accept_terms":"yes","csrf_token":token})
            first_otp = sender.call_args.kwargs["otp_code"]
            token = self.csrf("/login")
            response = self.client.post("/resend-verification", data={"email":"new@example.com","csrf_token":token})
            self.assertEqual(response.status_code, 200)
            second_otp = sender.call_args.kwargs["otp_code"]
        token = self.csrf("/login")
        self.assertEqual(self.client.post("/verify-email", data={"email":"new@example.com","otp":first_otp,"csrf_token":token}).status_code, 400)
        token = self.csrf("/login")
        self.assertEqual(self.client.post("/verify-email", data={"email":"new@example.com","otp":second_otp,"csrf_token":token}).status_code, 302)

    def test_csrf_and_security_headers(self):
        self.create_user(); self.login()
        self.assertEqual(self.client.post("/goals", data={}).status_code, 400)
        response = self.client.get("/dashboard")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])

    def test_admin_permissions_user_control_and_backup(self):
        admin_id = self.create_user(admin=True)
        target_id = self.create_user("member@example.com")
        token = self.login()
        for path in ("/admin","/admin/users","/admin/resources","/admin/errors","/admin/operations"):
            self.assertEqual(self.client.get(path).status_code, 200, path)
        response = self.client.post(f"/admin/users/{target_id}/suspend", data={"csrf_token":token})
        self.assertEqual(response.status_code, 302)
        conn = sqlite3.connect(application.DB_PATH)
        self.assertEqual(conn.execute("SELECT is_suspended FROM users WHERE id=?",(target_id,)).fetchone()[0], 1)
        self.assertGreater(conn.execute("SELECT COUNT(*) FROM audit_logs WHERE admin_id=?",(admin_id,)).fetchone()[0], 0)
        conn.close()
        token = self.csrf("/admin/operations")
        response = self.client.post("/admin/backups", data={"csrf_token":token})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(list(application.BACKUP_DIR.glob("*.db")))
        token = self.csrf("/admin/resources")
        response = self.client.post("/admin/resources", data={"title":"Reviewed guide","category":"Safety",
            "summary":"A reviewed safety guide.","reading_time":"4 min","source_name":"Example Health",
            "external_url":"https://example.com/guide","csrf_token":token})
        self.assertEqual(response.status_code,302)
        token = self.csrf("/admin/operations")
        self.assertEqual(self.client.post("/admin/ai/toggle",data={"csrf_token":token}).status_code,302)

    def test_non_admin_cannot_access_control_room(self):
        self.create_user(); self.login()
        for path in ("/admin","/admin/users","/admin/resources","/admin/errors","/admin/operations"):
            self.assertEqual(self.client.get(path).status_code,403,path)

    def test_profile_photo_signature_validation(self):
        self.create_user(); token = self.login()
        response = self.client.post("/settings", data={"section":"profile","full_name":"Admin User","display_name":"Admin",
            "email":"admin@example.com","timezone":"Asia/Calcutta","csrf_token":token,
            "photo":(io.BytesIO(b"not-an-image"),"fake.png")}, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 302)
        with application.app.app_context():
            row=application.db().execute("SELECT photo FROM users WHERE email='admin@example.com'").fetchone()
            self.assertEqual(row["photo"], "")


if __name__ == "__main__":
    unittest.main()
