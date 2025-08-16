import datetime
import random
import string
import uuid
from zoneinfo import ZoneInfo
from pynamodb.models import Model
from pynamodb.attributes import (
    TTLAttribute,
    UnicodeAttribute,
)
import os


class UserMfa(Model):
    class Meta:
        table_name = "user_mfa"
        region = "ap-northeast-1"
        read_capacity_units = 1
        write_capacity_units = 1
        host = os.getenv("DYNAMO_DB_HOST")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        ttl_attribute = "expires"

    login_id = UnicodeAttribute(hash_key=True)
    mfa_id = UnicodeAttribute(range_key=True)
    mfa_code = UnicodeAttribute()
    expires = TTLAttribute()

    def set_data(self):
        self.mfa_id = str(uuid.uuid4())
        self.mfa_code = "".join(
            random.choices(
                string.ascii_letters + string.digits, k=int(os.getenv("MFA_DIGIT"))
            )
        )
        self.expires = datetime.datetime.now(
            ZoneInfo("Asia/Tokyo")
        ) + datetime.timedelta(minutes=10)
