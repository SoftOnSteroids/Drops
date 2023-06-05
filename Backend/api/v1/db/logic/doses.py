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

def search_doses_by_date_range(date_min: date, date_max: date | None) -> list[Dose] | None:
    """
    Search doses in database by date range.

    If date_max is None, it will be set to the current date.

    If date_min is greater than date_max, the function will swap them.
    """
    if date_max is None:
        date_max = datetime.now().date()

    if date_min > date_max:
        temp_date = date_min
        date_min = date_max
        date_max = temp_date

    doses_found = doses_schema(db_client.doses.find({"date_start": 
                                              {"$gte": datetime.combine(date_min, datetime.min.time()), 
                                               "$lte": datetime.combine(date_max, datetime.max.time())}
                                               }))

    if doses_found:
        doses = []
        for i in range(len(doses_found)):
            doses.append(Dose(**doses_found[i]))

        return doses