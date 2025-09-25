from flask import Flask, render_template
from password_generator import bp as password_bp

def create_app():
    app = Flask(__name__)

    # landing page
    @app.get("/")
    def index():
        return render_template("index.html")

    # mount tools
    app.register_blueprint(password_bp, url_prefix="/password")

    # healtz ping page
    @app.get("/healthz")
    def healthz():
        return "OK", 200

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
