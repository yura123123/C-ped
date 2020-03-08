from os import path

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO


def main(CFG):
    # The path to directory this code is ran in.
    CUR_PATH = path.dirname(path.abspath(__file__))

    server_CFG = CFG["Server"]

    # The IP to run server on.
    IP = server_CFG.get("ip", "0.0.0.0")
    # The port on which server is hosted.
    PORT = server_CFG.getint("port", 8080)
    # !!! FUN !!! DEBUG MODE. Gives access to most stuff on server,
    # very dangerous to be put on production.
    DEBUG = server_CFG.getboolean("debug", False)
    # Secret key used to encrypt requests and stuff.
    SECRET_KEY = server_CFG.get("secret_key")

    # The directory with all web-related templates.
    template_dir = path.join(CUR_PATH, "../templates")
    # The directory for static files, such as .css, client-side JavaScript.
    static_dir = path.join(CUR_PATH, "../static")

    app = Flask(__name__, template_folder=template_dir, static_url_path="")
    app.config["SECRET_KEY"] = SECRET_KEY

    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    socketio = SocketIO(app)

    @app.after_request
    def after_request(response):
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"
        # response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        # response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/static/<path:path>")
    def send_static(path):
        return send_from_directory(static_dir, path)

    print("=====\n" + "Server starting on " + str(IP) + ":" + str(PORT))

    socketio.run(app, host=IP, port=PORT, debug=DEBUG)
