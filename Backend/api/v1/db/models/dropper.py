from pydantic import BaseModel
from pymongo import IndexModel, ASCENDING
from datetime import date, datetime
from v1.db.client import db_client
from v1.db.models.dose import Dose

class Dropper(BaseModel):
    id: str | None = None
    name: str | None = None
    description: str | None = None
    code: str | None = None
    place_apply: int | None = None
    frequency: int | None = None
    start_datetime: datetime | None = None
    end_day: date | None = None
    date_expiration: date | None = None
    doses: list[Dose] | None = None

    def getDoses(self, start: datetime, end: datetime) -> list[Dose]:
        return [Dose(dropper_id="fake dose", application_datetime=datetime.now())]

index = IndexModel([("name", ASCENDING), ("date_expiration", ASCENDING)], 
                   unique=True, 
                   name="name_date_expiration_unique")
db_client.droppers.create_indexes([index])
# db_client.droppers.create_index("code", unique=True)