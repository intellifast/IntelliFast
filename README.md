# IntelliFast

A full Flask + SQLite intermittent-fasting tracker with account onboarding, a live fasting timer, editable history, batch import, computed analytics and streaks, goals, achievements, buddy invitations, curated learning resources, reminders, reports, settings, and CSV export.

## AI Buddy testing

Lumi, the in-app AI fasting buddy, uses Gemini through the Flask server. Create a local `.env` file containing:

```text
GEMINI_API_KEY=your-new-key-here
```

Restart the app after saving. The key stays server-side and `.env` is excluded by `.gitignore`. Lumi receives only relevant fasting summaries—not the user's email, password, or other account credentials. For a different compatible Gemini model, optionally add `GEMINI_MODEL=model-name`.

## Run locally

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The database is created automatically as `intellifast.db`.

## Production deployment

Set a long random `SECRET_KEY`, serve behind HTTPS, and run the WSGI app with Waitress:

```powershell
$env:SECRET_KEY = "replace-with-a-long-random-secret"
waitress-serve --host=127.0.0.1 --port=5000 app:app
```

Put a reverse proxy such as IIS or nginx in front for TLS and static-file caching. Registration and password reset are intentionally unavailable when transactional email is not configured; secure links are never displayed in the interface.

Production account flows require these environment values:

```text
APP_ENV=production
APP_BASE_URL=https://your-domain.example
SECRET_KEY=a-long-random-secret
BREVO_API_KEY=your-brevo-api-key
MAIL_FROM_EMAIL=a-sender-verified-in-brevo@example.com
MAIL_FROM_NAME=IntelliFast
```

Promote an existing, verified account to administrator from the server console:

```bash
flask --app app promote-admin --email account@example.com
```

The private `/admin` area provides user controls, registration/activity metrics, resource management, error review, AI availability and usage, consistent SQLite backups, operational status and an administrator audit trail.

## Verification

The app exposes `GET /health`. Functional checks should cover registration, onboarding, timer start/pause/resume/complete, manual history, imports, analytics pages, goals, buddies, settings, and CSV export.
