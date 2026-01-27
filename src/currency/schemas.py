import datetime

from pydantic import BaseModel


class PriceResponse(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True