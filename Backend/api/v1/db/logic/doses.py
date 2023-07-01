from v1.db.client import db_client
from v1.db.models.dose import Dose
from v1.db.helpers import clean_query

def get_doses(dict_url: dict) -> list[Dose] | None:
    """
    Search doses in database.
    """
    query = clean_query(dict_url)
    query.update({"$unwind": "$doses"})
    query.update({"$match": {}})
    if "dropper_id" in query:
        query["$match"].update({"doses.dropper_id": query["dropper_id"]})
        del(query["dropper_id"])
    if "dropper_name" in query and query["dropper_name"]:
        print(f"dropper_name: {query['dropper_name']}")
        query["$match"].update({"name": query["dropper_name"]})
        del(query["dropper_name"])
    if "application_datetime" in query:
        query["$match"].update({"doses.application_datetime": query["application_datetime"]})
        del(query["application_datetime"])
    if "end" in query or "start" in query:
        query["$match"].update({"doses.application_datetime": {}})
        if "start" in query:
            query["$match"]["doses.application_datetime"].update({"$gte": query["start"]})
            del(query["start"])
        if "end" in query:
            query["$match"]["doses.application_datetime"].update({"$lte": query["end"]})
            del(query["end"])
    query.update({"$project": {"_id": 0, "doses": 1}})
    doses_db = db_client.droppers.aggregate([{k: v} for k,v in query.items()])
    return [Dose.parse_obj(dose_db["doses"]) for dose_db in doses_db] if doses_db else None