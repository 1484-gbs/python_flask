from flask_jwt_extended import create_access_token, create_refresh_token
from pynamodb.exceptions import DoesNotExist
from werkzeug.exceptions import BadRequest

from flask_app.models.dynamodb.user_mfa import UserMfa


class MfaCreateToken:
    def execute(self, login_id, mfa_id, mfa_code):
        try:
            user_mfa = UserMfa.get(hash_key=login_id, range_key=mfa_id)
        except DoesNotExist:
            raise BadRequest("invalid request.")

        if user_mfa.mfa_code != mfa_code:
            raise BadRequest("incorrect mfa_code.")

        access_token = create_access_token(identity=login_id)
        refresh_toen = create_refresh_token(identity=login_id)

        user_mfa.delete()

        return access_token, refresh_toen
