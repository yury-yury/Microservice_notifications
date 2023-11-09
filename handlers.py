from typing import Optional

from fastapi import APIRouter, Depends, Query, Body

from schemas import RequestCreate, ResponseCreate, ResponseList
from services import Service

router = APIRouter()


@router.post("/create", response_model=ResponseCreate)
async def create(data: RequestCreate = Body(summary='Requested data to create a new notification.'),
                 service: Service = Depends()) -> ResponseCreate:
    """
    The asynchronous create function defines the application endpoint for processing a POST request
    to the /create URL. Takes a RequestCreate object from the request body as parameters,
    and an object of the Service class as a dependency. When requested, it calls the asynchronous
    create function of the Serice class. The result is returned as an object of the ResponseCreate class.
    """
    return await service.create(data)


@router.get("/list", response_model=ResponseList)
async def listing(
    user_id: str = Query(description="The User ID"),
    skip: Optional[int] = Query(
        description="Number of notifications to ignore", default=0),
    limit: Optional[int] = Query(
        description="Number of notifications that should be returned", default=10),
    service: Service = Depends()) -> ResponseList:
    """
    The asynchronous listing function defines the application endpoint for processing
    a GET request to the /list URL. Takes query parameters as arguments,
    and a Service class object as a dependency. When requested, it calls the asynchronous function
    list_notifications of the Service class. The result is returned as an object of the ResponseList class.
    """
    return await service.list_notifications(user_id, skip, limit)


@router.post("/read", response_model=ResponseCreate)
async def reader(
    user_id: str = Query(description="The User ID"),
    notification_id: str = Query(description="Notification ID"),
    service: Service = Depends(),
) -> ResponseCreate:
    """
    The asynchronous reader function defines the application endpoint for processing
    a request using the POST method to the /read URL. Takes query parameters as arguments,
    and a Service class object as a dependency. When requested, it calls the asynchronous
    function reader of the Service class. The result is returned as an object of the ResponseCreate class.
    """
    return await service.reader(user_id, notification_id)
