from flask_app import app
from create_dynamo_table import create_dynamo_table


if __name__ == "__main__":
    create_dynamo_table
    app.run()
