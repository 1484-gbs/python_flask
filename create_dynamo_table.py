from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.dynamodb.user import User


if __name__ == "__main__":
    if not ChatHistory.exists():
        ChatHistory.create_table()
    if not User.exists():
        User.create_table()
