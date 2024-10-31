from pydantic import BaseModel
from typing import List
from typing import Optional

class Coord(BaseModel):
    lat: float
    lng: float
class Region(BaseModel):
    coords: List[Coord]
    #name: str | None
    name: Optional[str]


