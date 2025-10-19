"""Test file with intentional security issues for testing."""

import subprocess

# B602: shell=True security issue
subprocess.call("ls -la", shell=True)

# B201: Flask debug mode
from flask import Flask  # noqa: E402

app = Flask(__name__)
app.run(debug=True)

# B105: Hardcoded password
PASSWORD = "admin123"

# B303: MD5 hash usage
import hashlib  # noqa: E402

hashlib.md5(b"data")
