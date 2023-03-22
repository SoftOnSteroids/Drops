from bson import ObjectId

def dropper_serializer(dropper: dict) -> dict:
    serialized_dropper={}
    if "id" in dropper.keys() and dropper["id"]:
        serialized_dropper.update({
            "_id": ObjectId(dropper["id"])
        })
        del dropper["id"]
    
    if "date_expiration" in dropper.keys() and dropper["date_expiration"]:
        serialized_dropper.update({
            "date_expiration": str(dropper["date_expiration"])
        })
        del dropper["date_expiration"]

    serialized_dropper.update({k: v for k, v in dropper.items() if v})
    
    return serialized_dropper

def droppers_serializer(droppers: list) -> list:
    return [dropper_serializer(dropper) for dropper in droppers]