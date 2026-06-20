"""WSGI entry point for the intelligain PythonAnywhere account."""

import os
import sys

PROJECT_HOME = "/home/intelligain/IntelliFast"
if PROJECT_HOME not in sys.path:
    sys.path.insert(0, PROJECT_HOME)

os.chdir(PROJECT_HOME)

from app import app as application  # noqa: E402

