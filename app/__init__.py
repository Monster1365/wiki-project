from flask import Flask
from flask_jwt_extended import JWTManager
import firebase_admin
from firebase_admin import credentials
import json
import base64
import os


def create_app():  
    app = Flask(__name__) 
    
    #환경변수에서 서비스 키와 OAuth 키 JSON 문자열을 읽어오기
    service_json = os.environ.get("SERVICE_ACCOUNT_JSON")
    oauth_json = os.environ.get("OAUTH_KEY_JSON")

    if not service_json or not oauth_json:
        raise RuntimeError("환경변수 SERVICE_ACCOUNT_JSON 또는 OAUTH_KEY_JSON이 설정되어 있지 않습니다.")

    service_dict = json.loads(service_json)
    oauth_dict = json.loads(oauth_json)

    cred = credentials.Certificate(service_dict)
    firebase_admin.initialize_app(cred)

    app.config["GOOGLE_CLIENT_ID"] = oauth_dict["web"]["client_id"]
    app.config["GOOGLE_CLIENT_SECRET"] = oauth_dict["web"]["client_secret"]
    app.config["JWT_SECRET_KEY"] = base64.b64encode(
        app.config["GOOGLE_CLIENT_SECRET"].encode()
    )
    app.secret_key = app.config["JWT_SECRET_KEY"] 

    jwt = JWTManager(app)

    from app.main import main as main_bp
    from app.auth import auth as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app