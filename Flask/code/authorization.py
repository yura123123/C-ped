import json

import global_vars

from flask import (
    redirect,
    request,
    session,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

from user_info import User_Info, Guest_Info


def is_authenticated(session_obj, request_obj):
    # or User_Info.get_by_session(session_obj, request_obj)
    return current_user.is_authenticated()


def setup_general_authorization(app, CFG):
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("."))


def setup_debug_authorization(app, CFG):
    @app.route("/debug_login")
    def debug_login():
        users_name = "Debug Profile"
        users_email = "debug@software.com"
        picture = "/static/resources/debug.png"
        unique_id = 1

        # Try to find our debug user.
        user = User_Info.get(user_id=unique_id)
        if user is None:
            user = User_Info(
                name=users_name,
                email=users_email,
                profile_pic=picture,
            )
            session_info = user.insert()
            session["user_id"] = user.user_id
            session["key"] = session_info["key"]

        # Begin user session by logging the user in
        login_user(user, remember=True)

        client = global_vars.clients_by_sid[request.sid]
        client.user_info = user
        client.client_info.user_id = user.user_id

        # Send user back to homepage
        return redirect(url_for(".me"))


def setup_google_authorization(app, CFG):
    # If any of this stuff is not set, consider
    # Google Authorization not being enabled.
    if "Google_Authorization" not in CFG.sections():
        return

    ga_CFG = CFG["Google_Authorization"]

    def get_google_provider_cfg():
        if ga_CFG is None:
            return None
        return requests.get(GOOGLE_DISCOVERY_URL).json()

    GOOGLE_CLIENT_ID = ga_CFG.get("google_client_id", "None")
    if GOOGLE_CLIENT_ID == "None":
        return

    GOOGLE_CLIENT_SECRET = ga_CFG.get("google_client_secret", "None")
    if GOOGLE_CLIENT_SECRET == "None":
        return

    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    # OAuth2 google client setup
    google_client = WebApplicationClient(GOOGLE_CLIENT_ID)

    @app.route("/login_google")
    def login_google():
        if is_authenticated(session, request):
            return redirect(url_for(".me"))

        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        if google_provider_cfg is None:
            return global_vars.redirect_error(
                "Google Authentication impossible.",
                error_code=400
            )

        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = google_client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)

    @app.route("/login_google/callback")
    def callback():
        if is_authenticated(session, request):
            return redirect(url_for(".me"))

        # Authorization code Google sent back.
        auth_code = request.args.get("code")

        google_provider_cfg = get_google_provider_cfg()
        if google_provider_cfg is None:
            return global_vars.redirect_error(
                "Google Authentication impossible.",
                error_code=400
            )

        # Getting a URL to hit  to get tokens that allow to ask for access.
        token_endpoint = google_provider_cfg["token_endpoint"]

        # Prepare and send a request to get the token.
        token_url, headers, body = google_client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=auth_code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )

        # Parse the token.
        google_client.parse_request_body_response(
            json.dumps(token_response.json()))

        # Getting a URL that will provide all user information.
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = google_client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(
            uri, headers=headers, data=body).json()

        # Checking whether user's email is actually verified.
        if userinfo_response.get("email_verified"):
            unique_id = userinfo_response["sub"]
            users_email = userinfo_response["email"]
            picture = userinfo_response["picture"]
            users_name = userinfo_response["given_name"]
        else:
            return global_vars.redirect_error(
                "User email not available or not verified by Google.", 400
            )

        # Try to find a User_Info matching this id in DB.
        user = User_Info.get(google_id=unique_id)
        if user is None:
            user = User_Info(
                name=users_name,
                email=users_email,
                profile_pic=picture,
                google_id=unique_id,
            )
            user.insert()
            """
            session_info = user.insert()
            session["user_id"] = user.user_id
            session["key"] = session_info["key"]
            """

        # Begin user session by logging the user in
        login_user(user, remember=True)

        client = global_vars.clients_by_sid[request.sid]
        client.user_info = user
        client.client_info.user_id = user.user_id

        # Send user back to homepage
        return redirect(url_for(".me"))


def setup_authorization(app, CFG):
    # User session management setup
    # https://flask-login.readthedocs.io/en/latest
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.anonymous_user = Guest_Info

    # Flask-Login helper to retrieve a user from our db
    @login_manager.user_loader
    def load_user(user_id):
        return User_Info.get(user_id)

    setup_general_authorization(app, CFG)
    if CFG["Server"]["Debug"]:
        setup_debug_authorization(app, CFG)
    setup_google_authorization(app, CFG)
