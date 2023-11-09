from datetime import datetime

import bson
from pymongo.results import InsertOneResult

from database import collection, async_collection
from schemas import RequestCreate, ResponseCreate, ResponseList, Notification, Key, RequestList, DataForResponseList
from settings import settings
from utils import get_random_number, send_email


class Service:
    """
    The Service class serves as a wrapper for methods containing all the business logic
    for processing requests to application endpoints.
    """
    @staticmethod
    async def create(data: RequestCreate) -> ResponseCreate:
        """
        The asynchronous create function is a method of the Settings class
        and is designed to process the requested data, implement functionality
        in accordance with the received data, generate a response
        and return it as a dataclass object. Accepts the following arguments as parameters:
        all data passed in the request body in the form of a RequestCreate object.
        Returns the result as an instance of the ResponseCreate dataclass.
        """
        query = {'_id': bson.objectid.ObjectId(data.user_id)}
        result: bool = True

        if await async_collection.count_documents(query) == 0:
            await async_collection.insert_one({
                "_id": bson.objectid.ObjectId(data.user_id),
                "email": settings.EMAIL
            })
        if data.target_id is None:
            target_id: InsertOneResult = await async_collection.insert_one({"email": settings.EMAIL})
            data.target_id = str(target_id.inserted_id)

        if data.key in [Key.registration, Key.new_login]:
            from_email: str = (await async_collection.find_one(bson.objectid.ObjectId(data.target_id)))['email']

            email: str = (await async_collection.find_one(query))['email']
            resp_post: bool = await send_email(from_email, email, data.key, data.key)
            result = resp_post

        if data.key in [Key.new_message, Key.new_post, Key.new_login]:



            new_notification = Notification(id=await get_random_number(),
                                            timestamp=datetime.now(),
                                            is_new= True,
                                            user_id=data.user_id,
                                            key=data.key,
                                            target_id=data.target_id,
                                            data=data.data)

            res_upd = await async_collection.update_one(query, {'$push': {'notifications': dict(new_notification)}})

            if not res_upd:
                result = False

            while len((await async_collection.find_one(query, {"notifications": 1, "_id": 0}))['notifications']) > 25:

                await async_collection.update_one(query, {'$pop': {'notifications': -1}})

        return ResponseCreate(success=result)

    @staticmethod
    async def list_notifications(
        user_id: str, skip: int = 0, limit: int = 10
    ) -> ResponseList:
        """
        The asynchronous function list_notifications is a method of the Settings class
        and is designed to process the requested data, implement functionality in accordance
        with the received data, generate a response and return it as a dataclass object.
        When called, it generates a list of notifications available to the user in the database
        and returns it taking into account the entered restrictions.
        Takes the following arguments as parameters:
            user ID as a string,
            the number of notifications that need to be skipped in the output, by default 0, and
            the limit on the number of notifications displayed by default, 10.
        Returns the result as an instance of the ResponseList dataclass.
        """
        query: dict = {'_id': bson.objectid.ObjectId(user_id)}
        if await async_collection.count_documents(query) == 0:
            await async_collection.insert_one({
                **query,
                "email": settings.EMAIL,
                "notifications": []
            })

        all_notifications = (await async_collection.find_one(query, {"notifications": 1, "_id": 0}))["notifications"]

        notifications = all_notifications[skip:(limit + skip)]

        new = 0
        for dict_ in all_notifications:
            if dict_['is_new']:
                new += 1

        response = ResponseList(
            success=True,
            data=DataForResponseList(
                elements=len(all_notifications),
                new=new,
                request=RequestList(
                    user_id=user_id,
                    skip=skip,
                    limit=limit
                ),
                list=notifications))

        return response

    @staticmethod
    async def reader(user_id: str, notification_id: str) -> ResponseCreate:
        """
        The asynchronous reader function is a method of the Settings class and is designed to process
        the requested data, implement functionality in accordance with the received data,
        generate a response and return it as a dataclass object. When called,
        updates the value of the is_new field in the found user document notification.
        Takes the following arguments as parameters:
            user ID as a string,
            notification ID as a string.
        Returns the result as an instance of the ResponseCreate dataclass.
        """
        query = {'_id': bson.objectid.ObjectId(user_id), 'notifications.id': notification_id}

        if await async_collection.count_documents(query) > 0:

            await async_collection.find_one_and_update(query, {'$set': {"notifications.$.is_new": False}})
            return ResponseCreate(success=True)

        return ResponseCreate(success=False)
