from typing import List, Optional

from pydantic import BaseModel


class BaseModelWithOptionals(BaseModel):
    def __init_subclass__(cls, optional_fields: List[str] = None) -> None:
        """
        allow some fields of subclass turn into optional
        """
        super().__init_subclass__()
        if optional_fields:
            for field in optional_fields:
                cls.__fields__[field].outer_type_ = Optional
                cls.__fields__[field].required = False
