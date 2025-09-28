from flask import Blueprint, jsonify, request
from flask_app.usecase.login_create_token import LoginCreateToken
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_app.usecase.login_refresh_token import LoginRefreshToken
from flask_app import csrf
from flask_app.usecase.mfa_create_token import MfaCreateToken
import os

api_login = Blueprint("api_login", __name__)
csrf.exempt(api_login)


@api_login.post("/login")
def post():
    post_data = request.get_json(force=True)
    login_id = post_data.get("login_id")
    password = post_data.get("password")
    if not login_id or not password:
        raise BadRequest("login_id and pasword is required.")
    is_mfa = bool(os.getenv("IS_MFA", "False"))
    ret_val1, ret_val2 = LoginCreateToken().execute(
        login_id=login_id, password=password, is_mfa=is_mfa
    )
    if is_mfa:
        return jsonify(dict(login_id=login_id, mfa_id=ret_val1, mfa_code=ret_val2))
    return jsonify(dict(access_token=ret_val1, refresh_token=ret_val2))


@api_login.post("/refresh_token")
@jwt_required(refresh=True)
def refresh():
    return jsonify(access_token=LoginRefreshToken().execute(get_jwt_identity()))


@api_login.post("/mfa")
def mfa():
    post_data = request.get_json(force=True)
    login_id = post_data.get("login_id")
    mfa_id = post_data.get("mfa_id")
    mfa_code = post_data.get("mfa_code")
    access_token, refresh_token = MfaCreateToken().execute(
        login_id=login_id, mfa_id=mfa_id, mfa_code=mfa_code
    )
    return jsonify(dict(access_token=access_token, refresh_token=refresh_token))


@api_login.errorhandler(400)
def error_handler(error):
    return jsonify(dict(message=error.description)), error.code


# @api_login.errorhandler(Exception)
# def exception_handler(error):
#     return jsonify(dict(message="internal server error.")), 500
