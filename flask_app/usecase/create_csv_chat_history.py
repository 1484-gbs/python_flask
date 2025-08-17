from flask_app.models.s3_client import S3Client
from flask_app.usecase.get_chat_history import GetChatHistory
import pandas as pd
import io


class CreateCsvChatHistory:
    def execute(self, chat_id, login_id):
        result = GetChatHistory().execute(chat_id=chat_id, login_id=login_id)
        df = pd.DataFrame(result)[["role", "message"]]
        df["message"] = df["message"].str.replace("<.*?>", "", regex=True)
        with io.BytesIO(
            bytes(df.to_csv(index=False, quoting=1).encode("utf-8"))
        ) as file:
            S3Client().upload(
                file=file,
                login_id=login_id,
                service_type="chat_history",
                filename=f"chat_history_{login_id}_{chat_id}.csv",
            )
