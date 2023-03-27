from pydantic import BaseModel
from datetime import date
from v1.db.client import db_client

class Dropper(BaseModel):
    id: str | None = None
    name: str
    code: str | None = None
    description: str | None = None
    cold_chain: bool | None = None
    volume: int | None = None
    date_expiration: date | None = None
    color: str | None = None

db_client.droppers.create_index("name", unique=True)
db_client.droppers.create_index("code", unique=True)