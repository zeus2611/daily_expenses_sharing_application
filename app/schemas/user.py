"""
app/schemas/user.py
This module contains the Pydantic models for the user 
in the daily expenses sharing application.
It includes the UserBase, UserCreate, and User models.
"""

from pydantic import BaseModel, EmailStr, StringConstraints
from typing_extensions import Annotated

class UserBase(BaseModel):
    """
    Base model for a user in the daily expenses sharing application.

    Attributes:
        email (EmailStr): The email of the user.
        name (str): The name of the user.
        mobile_number (Annotated[str, StringConstraints(max_length=10, 
                        min_length=10, pattern=r'^\d{10}$')]): The mobile number of the user.
    """

    email: EmailStr
    name: str
    mobile_number: Annotated[str, StringConstraints(max_length=10, min_length=10, pattern=r'^\d{10}$')]

class UserCreate(UserBase):
    """
    Model for creating a new user in the daily expenses sharing application.
    Inherits from UserBase.

    Attributes:
        password (str): The password of the user.
    """

    pass

class User(UserBase):
    """
    Model for a user in the daily expenses sharing application.
    Inherits from UserBase.

    Attributes:
        id (int): The ID of the user.
    """

    id: int

    class Config:
        """
        Configuration class for the User model.
        """
        orm_mode = True
