from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(oid=v):
            raise TypeError('Invalid objectid')
        return str(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")