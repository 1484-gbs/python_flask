from flask_login import login_user
from pynamodb.exceptions import DoesNotExist
from werkzeug.exceptions import BadRequest
from flask_app.forms.login_form import LoginForm
from flask_app.models.dynamodb.user import User
from werkzeug.security import check_password_hash

from flask_app.models.dynamodb.user_mfa import UserMfa


class Mfa:
    def execute(self, login_id, mfa_id, mfa_code):
        try:
            user_mfa = UserMfa.get(hash_key=login_id, range_key=mfa_id)
        except DoesNotExist:
            raise BadRequest("invalid request.")

        if user_mfa.mfa_code != mfa_code:
            raise BadRequest("incorrect mfa_code.")

        login_user(User.get(login_id))

        user_mfa.delete()
