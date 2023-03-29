from v1.db.client import db_client
from v1.db.models.dose import Dose
from v1.db.schemas.dose import doses_schema
from v1.db.serializers.dose import dose_serializer
from v1.db.helpers import build_query
from datetime import date, datetime

def search_doses(doses_query: dict) -> list[Dose] | None:
    """
    Search doses in database.
    """
    doses = doses_schema(db_client.doses.find( dose_serializer(doses_query) ))

    if doses:
        doses_found = []
        for i in range(len(doses)):
            doses_found.append(Dose(**doses[i]))
        return doses_found

def search_doses_by_date_range(date_start: date, date_end: date) -> list[Dose] | None:
    """
    Search doses in database by date range.

    If date_start is greater than date_end, the function will swap them.
    """
    if date_start > date_end:
        temp_date = date_start
        date_start = date_end
        date_end = temp_date

    doses = doses_schema(db_client.doses.find({"date_start": 
                                              {"$gte": datetime.combine(date_start, datetime.min.time()), 
                                               "$lte": datetime.combine(date_end, datetime.max.time())}
                                               }))

    if doses:
        doses_found = []
        for i in range(len(doses)):
            doses_found.append(Dose(**doses[i]))

        return doses_found