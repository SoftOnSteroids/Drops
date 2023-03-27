def build_query(dict_path: dict) -> dict:
    """
    Cleans the query from None (null) values and 'id' key (keeps '_id' key).
    
    Returns a dict with the cleaned query.
    """
    query = {}
    if "id" in dict_path.keys() and (dict_path["id"] == None or dict_path["id"] == ""):
        del dict_path["id"]
    query.update({k:v for k,v in dict_path.items() if v!=None})
    return query