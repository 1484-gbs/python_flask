import os
from flask import Flask
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)


from flask_app.controller.index import func_index
from flask_app.controller.hoge import func_hoge
from flask_app.controller.chat import func_chat

app.register_blueprint(func_index)
app.register_blueprint(func_hoge)
app.register_blueprint(func_chat)
