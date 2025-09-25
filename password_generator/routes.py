from flask import render_template, request, jsonify
from .decode import decode, decode_url
from . import bp

@bp.route("/", methods=["GET", "POST"])
def page():
    # server-rendered flow (no JS):
    result = error = None
    if request.method == "POST":
        input_type = request.form.get("input_type", "text")
        body = (request.form.get("input_body") or "").strip()
        try:
            complexity = max(2, min(6, int(request.form.get("complexity", 4))))
        except ValueError:
            error = "Invalid complexity"
        if not body:
            error = "Input is required"
        else:
            try:
                result = decode(body, complexity) if input_type == "text" else decode_url(body, complexity)
            except Exception as e:
                error = str(e)
    return render_template("password.html", result=result, error=error)
