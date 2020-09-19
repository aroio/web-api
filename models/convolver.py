from typing import Optional, List
from pydantic import BaseModel


class Filter(BaseModel):
    is_active: bool = False
    coeff_name: Optional[str] = None
    coeff_comment: Optional[str] = None
    coeff_att: Optional[str] = None
    coeff_delay: Optional[str] = None


class FilterInDb(Filter):
    id: int = 0


class ConvolverConfig(BaseModel):
    debug: bool = False
    load_prefilter: bool = False
    brutefir: bool = False
    def_coeff: Optional[int] = 0
    filters: List[FilterInDb] = []
