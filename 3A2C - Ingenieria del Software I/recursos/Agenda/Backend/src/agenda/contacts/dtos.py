"""Defines data transfer objects for contacts (DTOs)"""

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import List, Optional


@dataclass
class ContactDTO:
    name: str
    lastname: str
    email: str
    phone_main: str
    phone_backup: Optional[str] = None
    tags: List[int] = dataclass_field(default_factory=list)
