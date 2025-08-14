import datetime
from zoneinfo import ZoneInfo
from flask import Blueprint, render_template
from flask_login import login_required

func_index = Blueprint("func_index", __name__)


@func_index.get("/")
@login_required
def index():
    return render_template("index.html")
