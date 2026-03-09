"""Define utility functions."""
from typing import List

from agenda.tags.services import TagService
from agenda.models.db import SessionLocal
from contextlib import suppress


def populate_tags(tags: List[str]):
    """
    populates database with a list of tags

    Parameters
    ----------
    tags : List[str]
        list of tags to populate database.
    """
    with SessionLocal() as db:
        tag_service = TagService(db)
        for tag_label in tags:
            with suppress(Exception):
                tag_id = tag_service.create_tag(label=tag_label)              
                print(f"Created tag {tag_label} with id {tag_id}!")

