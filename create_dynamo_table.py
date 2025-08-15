from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.dynamodb.user import User
from werkzeug.security import generate_password_hash

if __name__ == "__main__":
    if not ChatHistory.exists():
        ChatHistory.create_table()
    if not User.exists():
        User.create_table()
        User(login_id="test", password=generate_password_hash("testtest")).save()
        User(login_id="test2", password=generate_password_hash("testtest2")).save()
