from datetime import datetime
from enum import Enum
from typing import Optional, Any, Dict, List

from pydantic import BaseModel, Field, field_validator


class Key(str, Enum):
    """
    The Key class is an Enum class that defines the valid values of the key field of the notification data schema.
    """
    registration = "registration"
    new_message = "new_message"
    new_post = "new_post"
    new_login = "new_login"


class Notification(BaseModel):
    """
    The Notification class is a data class that describes the schema
    and data types of an object of embedded database documents.
    """
    id: str
    timestamp: datetime
    is_new: bool
    user_id: str
    key: Key
    target_id: str
    data: Optional[Dict[str, Any]]


class RequestCreate(BaseModel):
    """
    The RequestCreate class inherits from the BaseModel base class from the pydantic module.
    Describes the structure and types of data received from the request body when creating a notification.
    Designed for validation, as well as convenient serialization and deserialization of data.
    """
    user_id: str
    target_id: Optional[str] = None
    key: Key
    data: Optional[Any] = None

    @field_validator("user_id")
    def val_id(cls, value):
        """
        The val_id function is intended to validate the value passed to the user_id field.
        Takes the field value as a parameter. Checks the length of a string.
        If the check is successful, it returns the resulting value, otherwise it raises a validation error.
        """
        if len(value) != 24:
            raise ValueError("")
        return value

    @field_validator("target_id")
    def val_tar_id(cls, value):
        """
        The val_tar_id function is intended to validate the value passed to the target_id field.
        Takes the field value as a parameter. Checks the length of a string.
        If the check is successful, it returns the resulting value, otherwise it raises a validation error.
        """
        if type(value) == str and len(value) != 24:
            raise ValueError("")
        return value


class ResponseCreate(BaseModel):
    """
    The ResponseCreate class inherits the BaseModel base class of the pydantic module.
    Describes the structure and data types that serve as an API response.
    Designed for verification, as well as convenient serialization and deserialization of data.
    """
    success: bool


class RequestList(BaseModel):
    """
    The RequestList class inherits from the BaseModel base class from the pydantic module.
    Describes the structure and types of data received from the request body when listing notifications.
    Designed for validation, as well as convenient serialization and deserialization of data.
    """
    user_id: str
    skip: int = 0
    limit: int = 10


class DataForResponseList(BaseModel):
    """
    The DataForResponseList class inherits the BaseModel base class of the pydantic module.
    Describes the structure and data types that values field data from class ResponseList.
    Designed for verification, as well as convenient serialization and deserialization of data.
    """
    elements: int
    new: int
    request: RequestList
    list: List[Notification] = Field(default_factory=list)


class ResponseList(BaseModel):
    """
    The ResponseList class inherits the BaseModel base class of the pydantic module.
    Describes the structure and data types that serve as an API response.
    Designed for verification, as well as convenient serialization and deserialization of data.
    """
    success: bool
    data: DataForResponseList  # = field(default_factory=dict)
