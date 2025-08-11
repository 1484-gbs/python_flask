from flask import Blueprint, jsonify, request
from flask_app.usecase.login_create_jwt import LoginCreateJwt
from werkzeug.exceptions import BadRequest

api_login = Blueprint("api_login", __name__)


@api_login.post("/login")
def post():
    post_data = request.get_json(force=True)
    login_id = post_data.get("login_id")
    password = post_data.get("password")
    if not login_id or not password:
        raise BadRequest("login_id and pasword is required.")
    token = LoginCreateJwt().execute(login_id=login_id, password=password)
    return jsonify(dict(token=token))


@api_login.errorhandler(400)
def error_handler(error):
    return jsonify(dict(message=error.description)), error.code


@api_login.errorhandler(Exception)
def exception_handler(error):
    return jsonify(dict(message="internal server error.")), 500
