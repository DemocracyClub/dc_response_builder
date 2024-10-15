from typing import List

from pydantic import BaseModel, validator


class Point(BaseModel):
    type: str
    coordinates: List[float]

    @validator("type")
    def validate_type(cls, v):
        if not v == "Point":
            raise ValueError("Point required")
        return v
