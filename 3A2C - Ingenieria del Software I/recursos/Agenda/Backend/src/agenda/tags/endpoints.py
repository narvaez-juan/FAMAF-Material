from typing import List

from fastapi import APIRouter, Depends

from agenda.models.db import get_db
from agenda.tags.models import Tag
from agenda.tags.schemas import TagSchema
from agenda.tags.services import TagService

tags_router = APIRouter()


@tags_router.get(path="")
async def retrieve_tags(db=Depends(get_db)) -> List[TagSchema]:
    """
    gets agenda available tags for contacts.

    Returns
    -------
    List[TagSchema]
        A list of available tags
    """
    return [TagSchema(id=tag.id, label=tag.label) for tag in TagService(db).get_all()]
