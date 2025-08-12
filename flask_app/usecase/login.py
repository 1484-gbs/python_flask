from flask_login import login_user
from pynamodb.exceptions import DoesNotExist
from werkzeug.exceptions import BadRequest
from flask_app.forms.login_form import LoginForm
from flask_app.models.dynamodb.user import User
from flask_jwt_extended import create_access_token


class Login:
    def execute(self, form: LoginForm):
        try:
            # ユーザー取得
            user = User.get(form.login_id.data)
        except DoesNotExist:
            raise BadRequest("incorrect login id or password.")

        # TODO
        if user.password != form.password.data:
            raise BadRequest("incorrect login id or password.")

        login_user(user)
