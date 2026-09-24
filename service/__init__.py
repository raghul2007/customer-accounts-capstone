"""Customer Accounts service package."""
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, content_security_policy=None)
CORS(app)
from service import routes  # noqa: E402,F401
