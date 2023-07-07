from fastapi import APIRouter, HTTPException, status, Query
from bson import ObjectId
from pymongo import ReturnDocument
from typing import Annotated
from v1.db.models.dropper import Dropper
from v1.db.client import db_client
from v1.db.logic.helpers import Helper
from v1.db.logic.dropper import DropperHelper
from datetime import date, datetime

router = APIRouter(prefix="/droppers",
                   tags=["droppers"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado."}})

@router.get("/")
async def f_droppers(id: Annotated[str | None, Query()] = None,
                    name: Annotated[str | None, Query()] = None,
                    code: Annotated[str | None, Query()] = None,
                    place_apply: Annotated[int | None, Query()] = None,
                    start_datetime: Annotated[datetime | None, Query()] = None,
                    end_day: Annotated[date | None, Query()] = None,
                    date_expiration: Annotated[date | None, Query()] = None
                     ) -> list[Dropper] | None:
    dict_path={"id": id,
             "name": name,
             "code": code,
             "place_apply": place_apply,
             "start_datetime": start_datetime,
             "end_day": end_day,
             "date_expiration": date_expiration
            }
    droppers_db = db_client.droppers.find(Helper.clean_query(dict_path))
    return [Dropper.parse_obj(dropper_db) for dropper_db in droppers_db]

@router.post("/", response_model=Dropper, status_code=status.HTTP_201_CREATED)
async def f_add_dropper(dropper: Dropper) -> Dropper | HTTPException:
    # Verify that no other dropper exist with same name or code
    query = {
        "name": dropper.name
        } if not dropper.code else {
        "$or": [{"name": dropper.name}, 
                {"code": dropper.code}]
        }
    if DropperHelper.search_dropper(query):
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="dropper with same name and/or code already exist"
            )
    if dropper.id: del(dropper.id)
    new_id = db_client.droppers.insert_one(document=dropper.dict()).inserted_id
    return Dropper.parse_obj(db_client.droppers.find_one({"_id": new_id}))

@router.put("/", response_model=Dropper, status_code=status.HTTP_200_OK)
async def f_modify_dropper(dropper: Dropper) -> Dropper | HTTPException:
    dropper_dict = {k: v for k, v in dropper.dict().items() if v is not None and k != "id"}

    if dropper_updated := db_client.droppers.find_one_and_update(
        {"_id": ObjectId(dropper.id) if dropper.id else None},
        {"$set": dropper_dict},
        return_document= ReturnDocument.AFTER
        ):
        return Dropper().parse_obj(dropper_updated)
    else:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, 
            detail="Dropper not found. Not modified."
            )

@router.delete("/", response_model=Dropper, status_code=status.HTTP_200_OK)
async def f_delete_dropper(dropper: Dropper) -> Dropper | HTTPException:
    if not (dropper_deleted := db_client.droppers.find_one_and_delete(
            {"_id": ObjectId(dropper.id)}
            )):
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, 
            detail="Dropper not found. Not deleted."
            )
    
    return Dropper.parse_obj(dropper_deleted)
