import os
from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

login = LoginManager(app)
login.login_view = "/login"
csrf = CSRFProtect(app)
jwt = JWTManager(app)

from flask_app.controller.index import func_index
from flask_app.controller.hoge import func_hoge
from flask_app.controller.chat import func_chat
from flask_app.controller.login import func_login
from flask_app.controller.api.chat import func_api_chat
from flask_app.controller.api.login import api_login

app.register_blueprint(func_index)
app.register_blueprint(func_hoge)
app.register_blueprint(func_chat)
app.register_blueprint(func_login)
app.register_blueprint(func_api_chat, url_prefix="/api/v1")
app.register_blueprint(api_login, url_prefix="/api/v1")
