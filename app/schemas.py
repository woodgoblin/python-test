from pydantic import BaseModel, Field, Extra
from typing import List, Optional
from datetime import date


class RatBase(BaseModel):
    birth_date: date = Field(examples=["1995-01-01", "2020-01-01"])
    courage: int = Field(examples=[2, 4])
    stupidity: int = Field(examples=[4, 8])
    is_eaten: bool = Field(examples=[True, False])
    cat_id: Optional[int] = None


class RatCreate(RatBase):
    pass


class Rat(RatBase):
    id: int = Field(examples=[1, 2])

    class Config:
        orm_mode = True
        extra = Extra.forbid  # this is a gem that really makes writing examples that don't match basic formats
        # IMPOSSIBLE YEAH


class CatBase(BaseModel):
    birth_date: date = Field(examples=["1990-01-01", "2022-01-01"])
    paws_quantity: int = Field(examples=[2, 4])
    name: str = Field(examples=["Whiskers", "Paws"])
    gender: str = Field(examples=["M", "F"])
    tails_quantity: int = Field(examples=[1, 2])


class CatCreate(CatBase):
    pass


class Cat(CatBase):
    id: int = Field(examples=[1, 2])
    rats_eaten: List[Rat] = Field(default_factory=list)

    class Config:
        orm_mode = True
        extra = Extra.forbid
