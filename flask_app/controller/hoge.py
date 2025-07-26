import logging
from flask import Blueprint, request
from flask_app.usecase.hoge_list import HogeList

func_hoge = Blueprint("func_hoge", __name__)


@func_hoge.get("/hoge")
def hoge():
    max = 50
    # TODO validation
    try:
        if request.args.get("max") is not None:
            max = int(request.args.get("max"))
            # TODO
            if max > 99999:
                raise Exception("maybe dead.")
    except:
        message = "invalid parameter."
        logging.exception(message)
        return message
    return (
        "<a href='/'>return.</a>" + HogeList().execute(max) + "<a href='/'>return.</a>"
    )
