from pynamodb.attributes import (
    BooleanAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.models import Model
from src.config import Configuration
from datetime import datetime, timezone
from src.constants import Constants


def get_current_time_utc():
    return datetime.now(timezone.utc)


class InstaImageModel(Model):
    class Meta:
        table_name = Constants.IMAGE_TABLE
        region = Configuration.REGION
        host = Configuration.LOCALSTACK_URL

    user_id = UnicodeAttribute(hash_key=True)
    image_id = UnicodeAttribute(range_key=True)
    image_s3_key = UnicodeAttribute(default="")
    name = UnicodeAttribute(default="")
    size = NumberAttribute(default=0)
    meta_data = MapAttribute(null=True)
    is_deleted = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(default=get_current_time_utc)
    created_by = UnicodeAttribute(default="")
