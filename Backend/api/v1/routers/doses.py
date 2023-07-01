from fastapi import APIRouter, status, HTTPException, Query
from typing import Annotated
from datetime import datetime
from v1.db.models.dose import Dose
from v1.db.client import db_client
from v1.db.schemas.dose import dose_schema
from v1.db.serializers.dose import dose_serializer
from v1.db.logic.doses import get_doses

router = APIRouter(prefix="/doses",
                   tags=["doses"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado."}})

def search_dose(dict_dose: dict) -> Dose | None:
    a_dose = db_client.doses.find_one(dict_dose)
    if a_dose:
        return Dose(**dose_schema(db_client.doses.find_one(dict_dose)))

@router.get("/", response_model= list[Dose] | None)
async def f_doses(dropper_id: Annotated[str | None, Query()] = None,
                  dropper_name: Annotated[str | None, Query()] = None,
                  application_datetime: Annotated[datetime | None, Query()] = None,
                  start: Annotated[datetime | None, Query()] = None,
                  end: Annotated[datetime | None, Query()] = None
                     ) -> list[Dose] | None:
    dict_url = {"dropper_id": dropper_id,
                 "dropper_name": dropper_name,
                 "application_datetime": application_datetime,
                 "start": start,
                 "end": end,
                 }
    return get_doses(dict_url)

@router.post("/", response_model=Dose, status_code=status.HTTP_201_CREATED)
async def f_add_dose(dose: Dose) -> Dose | HTTPException:
    if "id" in dict(dose):
        dose.id = None
    dose_serialized = dose_serializer(dict(dose))
    
    # Varify that no other dose exist for same dropper at same time
    if "dropper_id" in dose_serialized.keys() and "application_time" in dose_serialized.keys() and search_dose({"application_time": dose_serialized["application_time"],
                    "dropper_id": dose_serialized["dropper_id"]}):
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="Dose with same dropper and application time already exist. Not added."
            )

    new_dose_id = db_client.doses.insert_one(dose_serialized).inserted_id

    return Dose(**dose_schema(db_client.doses.find_one({"_id": new_dose_id})))

# @router.put("/", response_model=Dose, status_code=status.HTTP_200_OK)
# async def f_update_dose(dose: Dose) -> Dose | HTTPException:
#     dose_updated = None
#     if dose.id:
#         dose_serialized = dose_serializer(dict(dose))
#         dose_updated = db_client.doses.find_one_and_update(
#             {"_id": dose_serialized["_id"]},
#             {"$set": clean_query(dose_serialized)},
#             return_document=ReturnDocument.AFTER
#             )
    
#     if dose_updated:
#         return Dose(**dose_schema(dose_updated))
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_304_NOT_MODIFIED,
#             detail="Dose not found. Not updated."
#         )

# @router.delete("/", response_model=Dose, status_code=status.HTTP_200_OK)
# async def f_delete_dose(dose: Dose) -> Dose | HTTPException:
#     if dose.id:
#         dose_deleted = db_client.doses.find_one_and_delete({"_id": ObjectId(dose.id)})
#         return Dose(**dose_schema(dose_deleted))
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_204_NO_CONTENT,
#             detail="Dose not found. Not deleted."
#         )
