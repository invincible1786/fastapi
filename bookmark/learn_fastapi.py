def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title();
    return full_name

print(get_full_name("john", "doe"))

# simple types
# int
# float
# bool
# bytes

# from typing import Any

# generics
# list - sqr bracket
# tuple
# set
# dict - 2 cols

# union
# def process_item(item: int | str):
#     print(item)

# none

# def say_hi(name: str | None = None):
#     if name is not None:
#         print(f"Hey {name}!")
#     else:
#         print("Hello World")

# can declare the type as a class
# class Person:
#     def __init__(self, name: str):
#         self.name = name

# def get_person_name(one_person: Person):
#     return one_person.name

# ==================================================

# fastapi dev main.py   
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
# automatic request parsing
# here the functions with paths are matched in order so declare accordingly
# the sooner the path matches that function will only be used

from enum import Enum

# for only specific types
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# path converted - final hyperparam set kardiya
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# REQUEST

from fastapi import FastAPI
from pydantic import BaseModel

# use none to make a data field optional
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

# fastapi apne aap req / query se parameters le lega


# RESPONSE

# defining the return type

# response model prioritised over type declaration - if type any of the two - no error

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr # for evaluating and checking an email input
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user



# DATA TYPES

# refer for data types -> https://fastapi.tiangolo.com/tutorial/extra-data-types/