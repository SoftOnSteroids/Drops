from pydantic import BaseModel
from datetime import date, datetime, time
from v1.db.models.dose import Dose

class Calendar(BaseModel):
    """
    Calendar model
    """
    name: str | None = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    description: str | None = None
    # day_start: date
    alarm: datetime
    doses: list