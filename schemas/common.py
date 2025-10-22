from bson import ObjectId
from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing import Annotated


PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v))]

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={ObjectId: str},
    )