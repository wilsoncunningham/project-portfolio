from flask import Blueprint
bp = Blueprint("password", __name__, template_folder="templates")
from .routes import bp
from . import routes  # noqa
