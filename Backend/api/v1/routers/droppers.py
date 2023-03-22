from fastapi import APIRouter, HTTPException, status, Query
from bson import ObjectId
from pymongo import ReturnDocument
from typing import Annotated
from v1.db.models.dropper import Dropper
from v1.db.client import db_client
from v1.db.schemas.dropper import dropper_schema, droppers_schema
from v1.db.serializers.dropper import dropper_serializer
from datetime import date

router = APIRouter(prefix="/droppers",
                   tags=["droppers"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado."}})

def search_dropper(dict_dropper: dict) -> Dropper | None:
    a_dropper = db_client.droppers.find_one(dict_dropper)
    if a_dropper:
        return Dropper(**dropper_schema(db_client.droppers.find_one(dict_dropper)))

@router.get("/")
async def f_droppers(id: Annotated[str | None, Query()] = None,
                    code: Annotated[str | None, Query()] = None,
                    name: Annotated[str | None, Query()] = None,
                    cold_chain: Annotated[bool | None, Query()] = None,
                    volume: Annotated[int | None, Query()] = None,
                    date_expiration: Annotated[date | None, Query()] = None,
                    color: Annotated[str | None, Query()] = None
                     ) -> list:
    query = dropper_serializer({"id": id,
             "code": code,
             "name": name,
             "cold_chain": cold_chain,
             "volume": volume,
             "date_expiration": date_expiration,
             "color": color
            })

    droppers = droppers_schema(db_client.droppers.find(query))
    
    return droppers

@router.post("/", response_model=Dropper, status_code=status.HTTP_201_CREATED)
async def f_add_dropper(dropper: Dropper) -> Dropper | HTTPException:
    dropper_dict = dropper_serializer(dict(dropper))
    
    # Varify that no other dropper exist with same name or code
    if search_dropper({"$or": [{"name": dropper_dict["name"]}, {"code": dropper_dict["code"]}]}):
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="dropper with same name and/or code already exist"
            )
    
    id = db_client.droppers.insert_one(dropper_dict).inserted_id
    
    new_dropper = dropper_schema(db_client.droppers.find_one({"_id": id}))
    
    return Dropper(**new_dropper)

@router.put("/", response_model=Dropper, status_code=status.HTTP_200_OK)
async def f_modify_dropper(dropper: Dropper) -> dict | HTTPException:
    dropper_dict = dropper_serializer(dict(dropper))

    dropper_found = db_client.droppers.find_one_and_update(
        {"_id": ObjectId(dropper.id)},
        {"$set": dropper_dict},
        return_document= ReturnDocument.AFTER
        )
    
    if not dropper_found:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, 
            detail="Dropper not found. Not modified."
            )
    
    return dropper_schema(dropper_found)

@router.delete("/", response_model=Dropper, status_code=status.HTTP_200_OK)
async def f_delete_dropper(dropper: dict) -> dict | HTTPException:
    
    dropper_found = db_client.droppers.find_one_and_delete(
        {"_id": ObjectId(dropper["id"])}
    )

    if not dropper_found:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, 
            detail="Dropper not found. Not deleted."
            )
    
    return dropper_schema(dropper_found)