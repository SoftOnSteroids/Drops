from bson import ObjectId
from datetime import datetime, date

def dose_serializer(dose: dict) -> dict:
    """
    Serializes a dose dict to a dose dict that can be used to send to the database.

    :raises TypeError: If the dose dict is not a dict
    """
    def format_date(dose_date: date) -> datetime:
        return datetime.combine(dose_date, datetime.min.time())
    
    serialized_dose={}
    if "id" in dose.keys() and dose["id"]:
        serialized_dose.update({
            "_id": ObjectId(dose["id"])
        })
        del dose["id"]
        
    if "dropper_id" in dose.keys() and dose["dropper_id"]:
        serialized_dose.update({
            "dropper_id": ObjectId(dose["dropper_id"])
        })
        del dose["dropper_id"]

    if "application_time" in dose.keys() and dose["application_time"]:
        serialized_dose.update({
            "application_time": datetime.combine(datetime.min, dose["application_time"])
        })
        del dose["application_time"]
    
    if "date_start" in dose.keys() and dose["date_start"]:
        serialized_dose.update({
            "date_start": format_date(dose["date_start"])
        })
        del dose["date_start"]
    
    if "date_end" in dose.keys() and dose["date_end"]:
        serialized_dose.update({
            "date_end": format_date(dose["date_end"])
        })
        del dose["date_end"]

    if "time_isolation" in dose.keys() and dose["time_isolation"]:
        serialized_dose.update({
            "time_isolation": dose["time_isolation"].total_seconds()
        })
        del dose["time_isolation"]
    
    if "time_separation_frequence" in dose.keys() and dose["time_separation_frequence"]:
        serialized_dose.update({
            "time_separation_frequence": dose["time_separation_frequence"].total_seconds()
        })
        del dose["time_separation_frequence"]

    serialized_dose.update({k: v for k, v in dose.items()})
    
    return serialized_dose


def doses_serializer(doses) -> list:
    return [dose_serializer(dose) for dose in doses]