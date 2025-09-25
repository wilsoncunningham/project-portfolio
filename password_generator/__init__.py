from flask import Blueprint
bp = Blueprint("password", __name__, template_folder="templates")
from . import routes  # noqa
