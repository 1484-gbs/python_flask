from zoneinfo import ZoneInfo
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    JSONAttribute,
    TTLAttribute,
)
import os
import datetime


class ChatHistory(Model):
    class Meta:
        table_name = "chat_history"
        region = "ap-northeast-1"
        read_capacity_units = 1
        write_capacity_units = 1
        host = os.getenv("DYNAMO_DB_HOST")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        ttl_attribute = "expires"

    login_id = UnicodeAttribute(hash_key=True)
    chat_id = UnicodeAttribute(range_key=True)
    history = JSONAttribute()
    expires = TTLAttribute()

    def save(self):
        self.expires = datetime.datetime.now(
            ZoneInfo("Asia/Tokyo")
        ) + datetime.timedelta(days=5)
        super(ChatHistory, self).save()
