def dropper_schema(dropper) -> dict:
    """
    Deserialize a dropper dict from the database to a dropper dict that can be used in the backend.
    E.g. as a param to a Dropper() constructor.

    :param dropper: The dropper dict from the database

    :return: The dropper dict that can be used in the backend

    :raises TypeError: If the dropper dict is not a dict
    """
    dropper_schema = {}

    if "_id" in dropper.keys() and dropper["_id"] != None and dropper["_id"] != "":
        dropper_schema.update({"id": str(dropper["_id"])})
        del dropper["_id"]
        if "id" in dropper.keys():
            del dropper["id"]

    # Add all other items
    dropper_schema.update({k: v for k, v in dropper.items()})

    return dropper_schema

def droppers_schema(droppers) -> list:
    return [dropper_schema(dropper) for dropper in droppers]