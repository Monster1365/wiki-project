from flask import Flask
from flask_jwt_extended import JWTManager
import firebase_admin
from firebase_admin import credentials
import json
import base64

def create_app():  
    app = Flask(__name__) 
    
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    with open("OAuthKey.json") as f:
        oauthKey = json.load(f)
        app.config["GOOGLE_CLIENT_ID"] = oauthKey["web"]["client_id"]
        app.config["GOOGLE_CLIENT_SECRET"] = oauthKey["web"]["client_secret"]
        app.config["JWT_SECRET_KEY"] = base64.b64encode(app.config["GOOGLE_CLIENT_SECRET"].encode())
        app.secret_key = app.config["JWT_SECRET_KEY"]

    jwt = JWTManager(app)

    from app.main import main as main_bp
    from app.auth import auth as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app