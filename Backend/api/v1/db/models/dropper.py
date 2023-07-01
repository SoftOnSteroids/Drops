from typing import Optional
from pydantic import BaseModel, Field
from pymongo import IndexModel, ASCENDING, ReturnDocument
from datetime import date, datetime, timedelta, time
from v1.db.client import db_client
from v1.db.models.dose import Dose
from v1.db.models.pyObjectId import PyObjectId
from v1.db.helpers import clean_query

class Dropper(BaseModel):
    id: PyObjectId | None = Field(default_factory=PyObjectId, alias="_id")
    name: str | None = None
    description: str | None = None
    code: str | None = None
    place_apply: int | None = None
    frequency: int | None = None
    start_datetime: datetime | None = None
    end_day: datetime | None = None
    date_expiration: datetime | None = None
    doses: list[Dose] | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

    def getDoses(self, start: datetime, end: datetime) -> list[Dose] | None:
        # If doses in range date exist return it, else create it.
        if self.doses == None or len(self.doses) == 0 or max(d.application_datetime for d in self.doses) < end:
            self.generateDoses(end=end)
        return self.doses
    
    # When frequency has changed remove doses from start onwards and create new ones
    
    def generateDoses(self, end: datetime, start: Optional[datetime] = None):
        if not start:
            start = self.start_datetime if self.start_datetime else datetime.combine(date.today(), time(hour=8))

        if self.frequency and self.doses:
            # Separate doses to keep
            keep_doses = list(filter(lambda dose: dose.application_datetime < start, self.doses))
            # Create doses from start to end.
            td_to_hours = lambda time_delta: time_delta.total_seconds() / (60 * 60)
            doses_in_delta = td_to_hours(end-start) / self.frequency
            for i in range(doses_in_delta):
                set_dose_time = lambda start, freq: start + timedelta(hours= freq * i)
                keep_doses.append(Dose(application_datetime= set_dose_time(start, self.frequency)))
            self.doses=keep_doses

            db_client.droppers.find_one_and_update(
                {"_id": self.id},
                {"$set": clean_query(self.dict())},
                return_document= ReturnDocument.AFTER
                )
            
index = IndexModel([("name", ASCENDING), ("date_expiration", ASCENDING)], 
                   unique=True, 
                   name="name_date_expiration_unique")
db_client.droppers.create_indexes([index])
# db_client.droppers.drop_index(index_or_name="code_1")
# db_client.droppers.create_index("code", unique=True)