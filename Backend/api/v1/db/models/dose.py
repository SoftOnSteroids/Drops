from pydantic import BaseModel, Field
from datetime import datetime
from v1.db.models.pyObjectId import PyObjectId

class Dose(BaseModel):
    dropper_id: PyObjectId | None = Field(default_factory=PyObjectId)
    application_datetime: datetime
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}