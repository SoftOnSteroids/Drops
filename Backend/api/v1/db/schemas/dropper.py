def dropper_schema(dropper) -> dict:
    return {
        "id": str(dropper["_id"]),
        "name": dropper["name"],
        "code": dropper["code"],
        "description": dropper["description"],
        "cold_chain": dropper["cold_chain"],
        "volume": dropper["volume"],
        "date_expiration": dropper["date_expiration"],
        "color": dropper["color"],
    }

def droppers_schema(droppers) -> list:
    return [dropper_schema(dropper) for dropper in droppers]