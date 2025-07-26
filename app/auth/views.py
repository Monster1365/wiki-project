from flask import redirect, url_for, current_app, request, jsonify, session
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from flask_jwt_extended import create_access_token
import firebase_admin.auth
from firebase_admin import firestore
import time
import requests
from . import auth

@auth.route('/login')
def login():
    redirect_uri = url_for('auth.google_callback', _external=True)
    client_id = current_app.config["GOOGLE_CLIENT_ID"]
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&scope=openid%20email%20profile&redirect_uri={redirect_uri}")

@auth.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for("main.index"))

@auth.route('/login/callback')
def google_callback():
    code = request.args.get('code')
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": current_app.config["GOOGLE_CLIENT_ID"],
        "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": url_for('auth.google_callback', _external=True),
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=data)
    response_json = response.json()
    token = response_json['id_token']

    idinfo = id_token.verify_oauth2_token(token, Request(), current_app.config["GOOGLE_CLIENT_ID"])

    try:
        user = firebase_admin.auth.get_user(idinfo['sub'])
    except firebase_admin.auth.UserNotFoundError:
        user = firebase_admin.auth.create_user(
        uid=idinfo['sub'], email=idinfo['email'], display_name=idinfo['name'])

    jwtKey = create_access_token(identity=idinfo['sub'] + str(time.time()))

    session["token"] = jwtKey

    # return f"Logined As {user_id}, mail: {user_email}, name: {user_name}"
    return redirect(url_for('main.index'))
