from datetime import timedelta
def dose_schema(dose) -> dict:
    """
    Deserialize a dose dict from the database to a dose dict that can be used in the backend.
    E.g. as a param to a Dose() constructor.

    :param dose: The dose dict from the database

    :return: The dose dict that can be used in the backend

    :raises TypeError: If the dose dict is not a dict
    """
    dose_schema = {}
    if "_id" in dose.keys() and dose["_id"] != None and dose["_id"] != "":
        dose_schema.update({"id": str(dose["_id"])})
        del dose["_id"]
        if "id" in dose.keys():
            del dose["id"]
    
    if "dropper_id" in dose.keys() and dose["dropper_id"] != None and dose["dropper_id"] != "":
        dose_schema.update({"dropper_id": str(dose["dropper_id"])})
        del dose["dropper_id"]

    if "application_time" in dose.keys() and dose["application_time"] != None and dose["application_time"] != "":
        dose_schema.update({"application_time": dose["application_time"].time()})
        del dose["application_time"]

    if "date_start" in dose.keys() and dose["date_start"] != None and dose["date_start"] != "":
        dose_schema.update({"date_start": dose["date_start"].date()})
        del dose["date_start"]
    
    if "date_end" in dose.keys() and dose["date_end"] != None and dose["date_end"] != "":
        dose_schema.update({"date_end": dose["date_end"].date()})
        del dose["date_end"]
    
    if "time_isolation" in dose.keys() and dose["time_isolation"] != None and dose["time_isolation"] != "":
        dose_schema.update({"time_isolation": timedelta(seconds=dose["time_isolation"])})
        del dose["time_isolation"]

    if "time_separation_frequence" in dose.keys() and dose["time_separation_frequence"] != None and dose["time_separation_frequence"] != "":
        dose_schema.update({"time_separation_frequence": timedelta(seconds=dose["time_separation_frequence"])})
        del dose["time_separation_frequence"]

    # Add all other items
    dose_schema.update({k: v for k, v in dose.items()})
    
    return dose_schema

def doses_schema(doses) -> list:
    return [dose_schema(dose) for dose in doses]