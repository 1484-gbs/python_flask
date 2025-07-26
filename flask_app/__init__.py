from flask import Flask

app = Flask(__name__)

from flask_app.controller.index import func_index
from flask_app.controller.hoge import func_hoge

app.register_blueprint(func_index)
app.register_blueprint(func_hoge)
