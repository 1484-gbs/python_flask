from flask_jwt_extended import create_access_token


class LoginRefreshToken:
    def execute(self, login_id):
        return create_access_token(identity=login_id)
