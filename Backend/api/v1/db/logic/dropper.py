from v1.db.client import db_client
from v1.db.logic.helpers import Helper
from v1.db.models.dropper import Dropper

class DropperHelper(Helper):
    @classmethod
    def search_dropper(cls, dict_dropper: dict) -> Dropper | None:
        """
        Search droppers in database.
        Params considered: dict_dropper is used as query.
        """
        if a_dropper := db_client.droppers.find_one(cls.clean_query(dict_dropper)):
            return Dropper.parse_obj(a_dropper)