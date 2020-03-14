from typing import List, Dict, Tuple, Optional
from pydantic import (
    BaseModel, ValidationError, PydanticValueError, conint, validator
)
from datetime import datetime

class NameWithoutSpace(PydanticValueError):
    code = "does_not_have_space"
    msg_template = "name doesn't have space, got '{wrong_value}'"

class Books(BaseModel):
    title: str
    authors: List[str]
    year: int
    publisher: str

class User(BaseModel):
    """Can be easily extensible with @dataclass for data parsing and validation"""
    id: int
    name: str = "John Doe"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []
    library: List[Books] = []

    @validator("name")
    def name_must_contain_space(cls, value):
        if ' ' not in value:
            raise NameWithoutSpace(wrong_value=value)  # ValueError
        return value


external_data = {
    "id": "123", 
    "name": "HadleyWickham",
    "signup_ts": "2019-06-01 12:22:00", 
    "friends": [1, 2, 3], 
    "library": [
        {
            "title": "Compositional Data Analysis",
            "authors": ["Pavlova"],
            "year": 2019,
            "publisher": "CRC",
        }
    ]
}

user = User(**external_data)
print(user.signup_ts)

# validation errors in a nice, clean format
try:
    User(signup_ts="broken", friends=[1, 2, "wrong"])
except ValidationError as e:
    print(e.json())

print(user.__fields_set__)
print(user.dict())
# print(user.schema())

