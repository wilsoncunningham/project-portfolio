from flask import render_template, request
from pprint import pprint
from . import bp

@bp.route("/", methods=["GET", "POST"])
def markov_switching():
    return render_template("markov_switching.html")
