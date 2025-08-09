from flask_app.models.dynamodb.chat_history import ChatHistory

if __name__ == "__main__":
    if not ChatHistory.exists():
        ChatHistory.create_table()
