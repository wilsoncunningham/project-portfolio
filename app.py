from flask import Flask, render_template
from password_generator import bp as password_bp
from stock_scraper import bp as scraper_bp
from markov_switching import bp as markov_switching_bp


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/bible")
    def bible():
        return render_template("bible.html")
    
    @app.get("/mathjax")
    def mathjax():
        return render_template("mathjax.html")

    # mount tools
    app.register_blueprint(password_bp, url_prefix="/password")
    app.register_blueprint(scraper_bp, url_prefix="/stock_scraper")
    app.register_blueprint(markov_switching_bp, url_prefix="/markov_switching")

    @app.get("/healthz")
    def healthz():
        return "OK", 200

    print(app.url_map)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
