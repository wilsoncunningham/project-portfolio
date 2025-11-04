from flask import Blueprint
bp = Blueprint("stock_scraper", __name__, template_folder="templates")
from .routes import bp
from . import routes 