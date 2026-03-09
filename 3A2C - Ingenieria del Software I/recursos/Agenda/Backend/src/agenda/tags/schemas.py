"""Defines tags endpoints schemas."""

from pydantic import BaseModel, Field, PositiveInt


class TagSchema(BaseModel):
    """Represent a tag."""

    id: PositiveInt
    label: str
