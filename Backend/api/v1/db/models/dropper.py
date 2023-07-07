from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, validator
from pymongo import IndexModel, ASCENDING, ReturnDocument
from datetime import date, datetime, timedelta, time
from v1.db.client import db_client
from v1.db.models.dose import Dose
from v1.db.models.pyObjectId import PyObjectId
from v1.db.logic.helpers import Helper

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

    def __init__(self, **data):
        super().__init__(**data)
        if "frequency" in data:
            self.generateDoses()
    
    def __setattr__(self, name, value):
        if name == "frequency":
            # self.generateDoses()
            print(f"Seetting {name} with value {value}")
        super().__setattr__(name, value)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

    def getDoses(self, start: datetime, end: datetime) -> list[Dose] | None:
        # If doses in range date exist return it, else create it.
        if self.doses == None or len(self.doses) == 0 or max(d.application_datetime for d in self.doses) < end:
            self.generateDoses(end=end)
        return self.doses
    
    def generateDoses(self, end: Optional[datetime] = None, start: Optional[datetime] = None):
        print("### Generating doses ###")
        if not start:
            start = self.start_datetime if self.start_datetime else datetime.combine(date.today(), time(hour=8))
        if not end:
            end = self.end_day if self.end_day else self.date_expiration if self.date_expiration else datetime.today()

        if self.frequency and self.doses:
            # Separate doses to keep
            keep_doses = list(filter(lambda dose: dose.application_datetime < start, self.doses))
            # Create doses from start to end.
            td_to_hours = lambda time_delta: time_delta.total_seconds() / (60 * 60)
            doses_in_delta = round(td_to_hours(end-start) / self.frequency)
            # print(f"start: {start}, end: {end}, frequency: {self.frequency}, td_to_hours: {round(td_to_hours(end-start))}, doses_in_delta: {doses_in_delta}")
            for i in range(doses_in_delta + 1):
                set_dose_time = lambda start, freq: start + timedelta(hours= freq * i)
                keep_doses.append(Dose(dropper_id=self.id, application_datetime= set_dose_time(start, self.frequency)))
                # print(f"set_dose_time: {set_dose_time(start, self.frequency)}, i: {i}")
            
            self.doses=keep_doses

            db_client.droppers.find_one_and_update(
                {"_id": ObjectId(self.id)},
                {"$set": Helper.clean_query(self.dict())},
                return_document= ReturnDocument.AFTER
                )

# index = IndexModel([("_id", ASCENDING), ("doses.application_datetime", ASCENDING)], 
#                    unique=True,
#                    name="dose_application_datetime")
# db_client.droppers.create_indexes([index])
# db_client.droppers.drop_index(index_or_name="name_date_expiration_unique")
# db_client.droppers.create_index("code", unique=True)