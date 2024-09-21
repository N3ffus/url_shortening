from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict


class UrlScheme(BaseModel):
    url: AnyHttpUrl


class UrlResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int
    url: AnyHttpUrl
    short_code: str
    created_at: datetime
    updated_at: datetime


class UrlStatsResponse(UrlResponse):
    access_count: int


class UrlNotFoundResponse(BaseModel):
    message: str
