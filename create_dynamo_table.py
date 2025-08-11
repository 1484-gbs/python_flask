from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.dynamodb.user import User


def create_dynamo_table():
    if not ChatHistory.exists():
        ChatHistory.create_table()
    if not User.exists():
        User.create_table()
