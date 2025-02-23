from pydantic import BaseModel
from typing import Optional

class DisasterData(BaseModel):
    disaster_type: Optional[str] = ""
    country: Optional[str] = ""
    region: Optional[str] = ""
    magnitude: Optional[str] = ""
    magnitude_scale: Optional[str] = ""
    cpi: Optional[str] = ""
    start_year: Optional[int] = None
    start_month: Optional[int] = None
    start_day: Optional[int] = None
    end_year: Optional[int] = None
    end_month: Optional[int] = None
    end_day: Optional[int] = None