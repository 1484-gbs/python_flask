from pynamodb.exceptions import DoesNotExist
from werkzeug.exceptions import BadRequest
from flask_app.models.dynamodb.user import User
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash

from flask_app.models.dynamodb.user_mfa import UserMfa


class LoginCreateToken:
    def execute(self, login_id, password, is_mfa):
        try:
            # ユーザー取得
            user = User.get(login_id)
        except DoesNotExist:
            raise BadRequest("incorrect login id or password.")

        if not check_password_hash(user.password, password):
            raise BadRequest("incorrect login id or password.")

        if is_mfa:
            # 既存mfaレコード削除
            for user_mfa in UserMfa.query(hash_key=login_id):
                user_mfa.delete()

            new_user_mfa = UserMfa(login_id=login_id)
            new_user_mfa.set_data()
            new_user_mfa.save()

            return new_user_mfa.mfa_id, new_user_mfa.mfa_code

        return create_access_token(identity=user.login_id), create_refresh_token(
            identity=user.login_id
        )
