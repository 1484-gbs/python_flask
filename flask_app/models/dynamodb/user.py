from zoneinfo import ZoneInfo
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
)
import os


class User(Model):
    class Meta:
        table_name = "user"
        region = "ap-northeast-1"
        read_capacity_units = 1
        write_capacity_units = 1
        host = os.getenv("DYNAMO_DB_HOST")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        # ttl_attribute = "expires"

    login_id = UnicodeAttribute(hash_key=True)
    password = UnicodeAttribute()
    # expires = TTLAttribute()
