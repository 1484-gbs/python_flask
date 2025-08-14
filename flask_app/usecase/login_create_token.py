from pynamodb.exceptions import DoesNotExist
from werkzeug.exceptions import BadRequest
from flask_app.models.dynamodb.user import User
from flask_jwt_extended import create_access_token, create_refresh_token


class LoginCreateToken:
    def execute(self, login_id, password):
        try:
            # ユーザー取得
            user = User.get(login_id)
        except DoesNotExist:
            raise BadRequest("incorrect login id or password.")

        # TODO
        if user.password != password:
            raise BadRequest("incorrect login id or password.")

        return create_access_token(identity=user.login_id), create_refresh_token(
            identity=user.login_id
        )
