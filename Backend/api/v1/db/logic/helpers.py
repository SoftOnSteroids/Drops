from datetime import datetime
from bson import ObjectId

class Helper():
    @classmethod
    def clean_query(cls, dict_path: dict) -> dict:
        """
        Cleans the query from None (null) values and 'id' key (keeps '_id' key).
        
        Returns a dict with the cleaned query.
        """
        query = {}
        if "id" in dict_path.keys() and (dict_path["id"] == None or dict_path["id"] == ""):
            del dict_path["id"]
        elif "id" in dict_path.keys():
            query.update({"_id": ObjectId(dict_path["id"])})
            del dict_path["id"]
        query.update({k:v for k,v in dict_path.items() if v!=None})
        return query
    
    @classmethod
    def format_date(cls, dose_date) -> datetime:
        """
        Formats a date or str(date) to a datetime object with time 00:00:00.

        :param dose_date: The date to format. Admisible as datetime.date object or str(date)
        """
        if type(dose_date) == str:
            dose_date = datetime.strptime(dose_date, "%Y-%m-%d")

        return datetime.combine(dose_date, datetime.min.time())