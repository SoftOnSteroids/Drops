from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class Dose(BaseModel):
    id: str | None = None
    dropper_id: str
    application_time: time | None = None
    place_to_apply: str | None = None
    date_start: date | None = None
    date_end: date | None = None
    day_start_time: datetime | None = None
    day_end_time: datetime | None = None
    frequence_in_day: int | None = None
    time_separation_frequence: timedelta | None = None
    time_isolation: timedelta | None = None
    priority: int | None = None
