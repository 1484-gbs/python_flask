from flask_login import login_user
from pynamodb.exceptions import DoesNotExist
from werkzeug.exceptions import BadRequest
from flask_app.forms.login_form import LoginForm
from flask_app.models.dynamodb.user import User
from werkzeug.security import check_password_hash

from flask_app.models.dynamodb.user_mfa import UserMfa


class Login:
    def execute(self, form: LoginForm, is_mfa=False):
        login_id = form.login_id.data
        try:
            # ユーザー取得
            user = User.get(login_id)
        except DoesNotExist:
            raise BadRequest("incorrect login id or password.")

        if not check_password_hash(user.password, form.password.data):
            raise BadRequest("incorrect login id or password.")

        if is_mfa:
            # 既存mfaレコード削除
            for user_mfa in UserMfa.query(hash_key=login_id):
                user_mfa.delete()

            new_user_mfa = UserMfa(login_id=login_id)
            new_user_mfa.set_data()
            new_user_mfa.save()

            return new_user_mfa.mfa_id, new_user_mfa.mfa_code

        login_user(user)
        return None, None
