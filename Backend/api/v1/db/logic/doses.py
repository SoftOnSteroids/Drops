from v1.db.client import db_client
from v1.db.models.dose import Dose
from v1.db.helpers import clean_query

def get_doses(dict_url: dict) -> list[Dose] | None:
    """
    Search doses in database.
    Params considered: dropper_id, dropper_name, application_datetime, start, end
    """
    dict_url = clean_query(dict_url)
    query = {
        "$unwind": "$doses",
        "$match": {},
        "$project": {"_id": 0, "doses": 1}
    }
    if "dropper_id" in dict_url:
        query["$match"].update({"doses.dropper_id": dict_url["dropper_id"]})
    if "dropper_name" in dict_url and dict_url["dropper_name"]:
        query["$match"].update({"name": dict_url["dropper_name"]})
    if "application_datetime" in dict_url:
        query["$match"].update({"doses.application_datetime": dict_url["application_datetime"]})
    if "end" in dict_url or "start" in dict_url:
        query["$match"].update({"doses.application_datetime": {}})
        if "start" in dict_url:
            query["$match"]["doses.application_datetime"].update({"$gte": dict_url["start"]})
        if "end" in dict_url:
            query["$match"]["doses.application_datetime"].update({"$lte": dict_url["end"]})
    doses_db = db_client.droppers.aggregate([{k: v} for k,v in query.items()])
    return [Dose.parse_obj(dose_db["doses"]) for dose_db in doses_db] if doses_db else None