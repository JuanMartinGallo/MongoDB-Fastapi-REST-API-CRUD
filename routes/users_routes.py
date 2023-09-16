# Importaciones de FastAPI
from fastapi import (
    APIRouter,
    Response,
    status,
    HTTPException,
    Body,
    Path,
    Query,
    Form,
    Header,
    Cookie,
    File,
    UploadFile,
    Request,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Importaciones relacionadas con la base de datos
from config.db import conn
from pymongo.errors import PyMongoError

# Importaciones relacionadas con los esquemas
from schemas.user import user_entity, users_entity

# Importaciones relacionadas con los modelos
from models.user import User

# Importaciones adicionales
from app import app
from pydantic import EmailStr
from typing import Optional, Required
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK
from email_validator import EmailNotValidError, validate_email


user = APIRouter()


@user.get(
    path="/users",
    response_model=list[User],
    tags=["Users"],
    summary="Get all users",
    response_description="List of users",
)
async def find_all_users():
    """
    Retrieves all users from the database.

    Returns:
    - list[User]: A list of User objects representing all the users in the database.
    """
    return users_entity(conn.local.user.find())


@user.post(
    path="/users",
    response_model=User,
    tags=["Users"],
    summary="Create a new user",
    response_description="User created",
)
async def create_users(user: User = Body(...)):
    """
    Creates a new user and stores it in the database.

    Parameters:
        user (User): The user object containing the user's details.

    Returns:
        JSONResponse: The response containing the newly created user entity.

    Raises:
        HTTPException: If the email provided is not a valid email.
    """
    try:
        validate_email(user.email)
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Not a valid email")
    new_user = dict(user)
    new_user["password"] = sha256_crypt.hash(new_user["password"])
    id = conn.local.user.insert_one(new_user).inserted_id
    new_user = conn.local.user.find_one({"_id": id})
    return JSONResponse(status_code=HTTP_201_CREATED, content=user_entity(new_user))


@user.get(
    path="/users/{id}",
    response_model=User,
    tags=["Users"],
    summary="Get a user",
    response_description="User details",
)
async def find_user(id: str = Path(...)):
    """
    Get a user.

    Args:
        id (str): The ID of the user.

    Returns:
        User: The details of the user.

    Raises:
        HTTPException: If the user is not found.
    """
    user = conn.local.user.find_one({"_id": ObjectId(id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_entity(conn.local.user.find_one({"_id": ObjectId(id)}))


@user.put(
    path="/users/{id}",
    response_model=User,
    tags=["Users"],
    summary="Update a user",
    response_description="User updated",
)
async def update_user(id: str = Path(...), user: User = Body(...)):
    """
    Updates a user in the database.

    Args:
        id (str): The ID of the user to be updated.
        user (User): The updated user object.

    Returns:
        User: The updated user object.

    Raises:
        HTTPException: If the user is not found or if there is an error updating the user in the database.
    """
    try:
        existing_user = conn.local.user.find_one({"_id": ObjectId(id)})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        new_user = dict(user)
        new_user["password"] = sha256_crypt.hash(new_user["password"])
        conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": new_user})
        return user_entity(conn.local.user.find_one({"_id": ObjectId(id)}))
    except PyMongoError as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating user in the database: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user, {e}")


@user.delete(
    path="/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Delete a user",
    response_description="User deleted",
)
async def delete_user(id: str = Path(...)):
    """
    Delete a user.

    Args:
        id (str): The ID of the user to delete.

    Returns:
        Response: The response indicating the success of the operation.
    """
    user_entity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.post(
    path="/login",
    status_code=HTTP_201_CREATED,
    tags=["Users"],
    summary="Login a user",
    response_description="User successfully logged in!",
)
async def login(
    username: str = Form(Required=True, default="test_updated"),
    password: str = Form(Required=True, default="test_password_updated"),
):
    """
    Logs in a user with the provided username and password.

    Parameters:
        username (str): The username of the user to log in. Default is "test_updated".
        password (str): The password of the user to log in. Default is "test_password_updated".

    Returns:
        dict: A dictionary containing the message "user {username} successfully logged in!".
    """
    try:
        user = conn.local.user.find_one({"name": username})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid password")
    except ConnectionError as ce:
        raise HTTPException(status_code=503, detail=f"Connection error: {ce}")
    except PyMongoError as pe:
        raise HTTPException(status_code=503, detail=f"PyMongo error: {pe}")
    return {"message": f"user {username} successfully logged in!!"}


async def verify_password(password: str, hashed_password: str) -> bool:
    return sha256_crypt.verify(password, hashed_password)


@user.post(
    path="/post-image",
    status_code=HTTP_200_OK,
    summary="Upload an image",
    response_description="Image uploaded!",
)
async def post_image(
    image: UploadFile = File(...),
):
    """
    Uploads an image file to the server.

    Parameters:
        - image (UploadFile): The image file to be uploaded.

    Returns:
        - dict: A dictionary containing the filename, format, and size of the uploaded image.
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=2),
    }
