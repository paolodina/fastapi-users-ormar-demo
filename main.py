from fastapi_users.authentication import CookieAuthentication

from fastapi_users import FastAPIUsers

import databases
import sqlalchemy
from fastapi import FastAPI
from fastapi_users import models
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase


app = FastAPI()
metadata = sqlalchemy.MetaData()
database = databases.Database("sqlite://./test.db")
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


class UserModel(OrmarBaseUserModel):
    class Meta:
        tablename = "users"
        metadata = metadata
        database = database


user_db = OrmarUserDatabase(UserDB, UserModel)

# ############### AUTH
SECRET = "SECRET"
auth_backends = []
cookie_authentication = CookieAuthentication(
    secret=SECRET, lifetime_seconds=3600,
    cookie_secure=False)
auth_backends.append(cookie_authentication)

# ############### ROUTING
fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

app.include_router(
    fastapi_users.get_auth_router(cookie_authentication),
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)
