# full pydantic - model - validation example

# from datetime import datetime
# from pydantic import BaseModel, PositiveInt, ValidationError

# class User(BaseModel):
#     id: int
#     name: str = 'John Doe'
#     signup_ts: datetime | None
#     tastes: dict[str, PositiveInt]


# external_data = {'id': 'not an int', 'tastes': {}}  

# try:
#     User(**external_data)  
# except ValidationError as e:
#     print(e.errors())
#     """
#     [
#         {
#             'type': 'int_parsing',
#             'loc': ('id',),
#             'msg': 'Input should be a valid integer, unable to parse string as an integer',
#             'input': 'not an int',
#             'url': 'https://errors.pydantic.dev/2/v/int_parsing',
#         },
#         {
#             'type': 'missing',
#             'loc': ('signup_ts',),
#             'msg': 'Field required',
#             'input': {'id': 'not an int', 'tastes': {}},
#             'url': 'https://errors.pydantic.dev/2/v/missing',
#         },
#     ]
#     """



# MODELS

from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    id: int
    name: str = 'Jane Doe'

    model_config = ConfigDict(str_max_length=10)  

user = User(id='123')

assert user.name == 'Jane Doe'  
assert user.id == 123  
assert isinstance(user.id, int)
assert user.model_dump() == {'id': 123, 'name': 'Jane Doe'} # converts into a dictionary


# models are mutable
# model properties - https://pydantic.dev/docs/validation/dev/concepts/models/#model-methods-and-properties
# data gets converted automatically to the designated type - can use strict - no type change on own
# extra data is ignored 

class Model(BaseModel):
    x: int
    model_config = ConfigDict(extra='allow') # - use for handling extra params - allow/ignore/forbid

m = Model(x=1, y='a')  
assert m.model_dump() == {'x': 1, 'y': 'a'}
assert m.__pydantic_extra__ == {'y': 'a'}

# nested models

from pydantic import BaseModel
class Foo(BaseModel):
    count: int
    size: float | None = None
class Bar(BaseModel):
    apple: str = 'x'
    banana: str = 'y'
class Spam(BaseModel):
    foo: Foo
    bars: list[Bar]

# dont define recursive models


# FIELDS

from pydantic import BaseModel, Field

class Model(BaseModel):
    name: str = Field(frozen=True)

# for reusing the same field over and over

from typing import Annotated
from pydantic import BaseModel, Field, WithJsonSchema

class Model(BaseModel):
    name: Annotated[str, Field(strict=True), WithJsonSchema({'extra': 'data'})]

# careful while using types and fields - dont mix

# int_list: list[Annotated[int, Field(gt=0)]]
# field_bad: Annotated[int, Field(deprecated=True)] | None = None  
# field_ok: Annotated[int | None, Field(deprecated=True)]


# VALIDATORS

# after

from typing import Annotated
from pydantic import AfterValidator, BaseModel, ValidationError

def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f'{value} is not an even number')
    return value  


class Model(BaseModel):
    number: Annotated[int, AfterValidator(is_even)]

try:
    Model(number=1)
except ValidationError as err:
    print(err)
    """
    1 validation error for Model
    number
      Value error, 1 is not an even number [type=value_error, input_value=1, input_type=int]
    """

# before

def ensure_list(value: Any) -> Any:  
    if not isinstance(value, list):  
        return [value]
    else:
        return value

class Model(BaseModel):
    numbers: Annotated[list[int], BeforeValidator(ensure_list)]

print(Model(numbers=2))
#> numbers=[2]
try:
    Model(numbers='str')
except ValidationError as err:
    print(err)  
    """
    1 validation error for Model
    numbers.0
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='str', input_type=str]
    """

# model validation

# before

from typing import Any

from pydantic import BaseModel, model_validator


class UserModel(BaseModel):
    username: str

    @model_validator(mode='before')
    @classmethod
    def check_card_number_not_present(cls, data: Any) -> Any:  
        if isinstance(data, dict):  
            if 'card_number' in data:
                raise ValueError("'card_number' should not be included")
        return data

# after

from typing_extensions import Self

from pydantic import BaseModel, model_validator


class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self