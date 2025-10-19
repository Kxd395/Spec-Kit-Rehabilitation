"""Test file with intentional security issues for testing."""
import subprocess

# B602: shell=True security issue
subprocess.call("ls -la", shell=True)

# B201: Flask debug mode
from flask import Flask
app = Flask(__name__)
app.run(debug=True)

# B105: Hardcoded password
PASSWORD = "admin123"

# B303: MD5 hash usage
import hashlib
hashlib.md5(b"data")
