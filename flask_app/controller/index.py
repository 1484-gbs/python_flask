import datetime
from zoneinfo import ZoneInfo
from flask import Blueprint

func_index = Blueprint("func_index", __name__)


@func_index.get("/")
def index():
    return (
        "<a href='/hoge'>Hellow World</a>"
        + "<br>"
        + str(datetime.datetime.now(ZoneInfo("Asia/Tokyo")))
        + "<br>"
        + "<a href='/chat'>chat</a>"
    )
