from enum import Enum
from pydantic import BaseModel
from datetime import datetime, timedelta


class Assets_type(Enum):
    SHARE = 1
    BOND = 2
    FUTURE = 3
    CURRENCY = 4
    ETF = 5
    OPTION = 6


class Asset(BaseModel):
    figi: str
    name: str
    asset_type: str
    price: float
    count: int


class Operation(BaseModel):
    figi: str
    name: str
    date: datetime
    count: int
    price: float
    buy: bool


class Payment_date(BaseModel):
    figi: str
    date: datetime
    amount: float
