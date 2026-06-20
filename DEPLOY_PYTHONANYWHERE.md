# Deploy IntelliFast to PythonAnywhere

Target account: `intelligain`

## 1. Upload and extract

Upload `IntelliFast-pythonanywhere.zip` in the PythonAnywhere **Files** tab. Open a Bash console and run:

```bash
cd /home/intelligain
unzip -o IntelliFast-pythonanywhere.zip -d IntelliFast
cd IntelliFast
```

## 2. Create the virtual environment

```bash
mkvirtualenv --python=/usr/bin/python3.13 intellifast-env
pip install -r /home/intelligain/IntelliFast/requirements.txt
```

If the environment already exists:

```bash
workon intellifast-env
pip install -r /home/intelligain/IntelliFast/requirements.txt
```

## 3. Create server secrets

In the **Files** tab, create `/home/intelligain/IntelliFast/.env`:

```text
SECRET_KEY=generate-a-long-random-value
GEMINI_API_KEY=paste-your-new-gemini-key
GEMINI_MODEL=gemini-2.5-flash
```

Never upload the local `.env` or expose this server file publicly.

## 4. Configure the web app

In the **Web** tab:

1. Add a new web app.
2. Choose **Manual configuration** and Python 3.13.
3. Set the virtualenv to `/home/intelligain/.virtualenvs/intellifast-env`.
4. Open the WSGI configuration file and replace its contents with:

```python
import sys

project_home = "/home/intelligain/IntelliFast"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

5. Add static mapping:
   - URL: `/static/`
   - Directory: `/home/intelligain/IntelliFast/static`
6. Press **Reload**.

The app creates `/home/intelligain/IntelliFast/intellifast.db` automatically on first import.

## 5. Verify

- Open `https://intelligain.pythonanywhere.com/health` and confirm `status: ok`.
- Register a new account and finish onboarding.
- Start and complete a test fast.
- Open AI Buddy and send a message to Lumi.
- Download a CSV export.

