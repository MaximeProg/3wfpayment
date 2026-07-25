import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CountryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    iso_code: str
    name: str
    is_active: bool
    synced_at: datetime


class NetworkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    country_id: uuid.UUID
    name: str
    code: str
    channel_type: str
    status: str
    synced_at: datetime


class ChannelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    country_id: uuid.UUID
    currency_code: str
    channel_type: str
    ramp_type: str
    status: str
    min_amount: Decimal | None
    max_amount: Decimal | None
    synced_at: datetime


class CurrencyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    country_id: uuid.UUID | None
    is_active: bool
