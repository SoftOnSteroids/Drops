from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class Dose(BaseModel):
    id: str | None = None
    dropper_id: str
    application_datetime: datetime | None = None
