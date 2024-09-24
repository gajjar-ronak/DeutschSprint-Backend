from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class Vocabulary(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId)
    word: str
    meaning: str
    level: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
