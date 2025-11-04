from flask import Blueprint, render_template, request
from .decode import decode

bp = Blueprint(
    "password",
    __name__,
    template_folder="templates",   # looks inside password_generator/templates
)

@bp.get("/")
def form():
    # renders the form
    return render_template("password.html")  # this file is in password_generator/templates

@bp.post("/generate")
def generate():
    input_body = request.form.get("input_body", "")
    try:
        complexity = int(request.form.get("complexity", 3))
    except ValueError:
        complexity = 3

    result = decode(input_body, complexity)
    # render the same page with the result block visible
    return render_template("password.html", result=result)
