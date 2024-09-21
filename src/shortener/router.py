from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.services.shortener_service import ShortenerService
from src.shortener.exceptions import UrlNotFoundError
from src.shortener.schemas import (UrlNotFoundResponse, UrlResponse, UrlScheme,
                                   UrlStatsResponse)
from src.shortener.utils import Shortener, get_shortener_service

router = APIRouter(prefix="/shorten", tags=["Shortener"])


@router.post("/", response_model=UrlResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url: UrlScheme,
    shortener_service: Annotated[ShortenerService, Depends(get_shortener_service)],
):
    short_url = await Shortener.create_url(shortener_service)
    result = await shortener_service.add_url(short_url, str(url.url))
    return result


@router.get(
    "/{short_url}",
    response_model=UrlResponse,
    responses={
        404: {
            "description": "Url not found",
            "content": {
                "application/json": {
                    "example": {"message": "Item not found"},  # Пример ответа
                    "schema": UrlNotFoundResponse.schema(),  # Схема ответа
                }
            },
        }
    },
)
async def get_original_url(
    short_url: str,
    shortener_service: Annotated[ShortenerService, Depends(get_shortener_service)],
):
    url = await shortener_service.get_url_by_short_code(short_url)
    if url is None:
        raise UrlNotFoundError()
    await shortener_service.increment_by_short_code(short_url, 1)
    return url


@router.put(
    "/{short_url}",
    response_model=UrlResponse,
    responses={
        404: {
            "description": "Url not found",
            "content": {
                "application/json": {
                    "example": {"message": "Item not found"},  # Пример ответа
                    "schema": UrlNotFoundResponse.schema(),  # Схема ответа
                }
            },
        }
    },
)
async def update_url(
    short_url: str,
    url: UrlScheme,
    shortener_service: Annotated[ShortenerService, Depends(get_shortener_service)],
):
    result = await shortener_service.update_by_short_code(short_url, str(url.url))
    if result is None:
        raise UrlNotFoundError()
    return result


@router.delete(
    "/{short_url}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "description": "Url not found",
            "content": {
                "application/json": {
                    "example": {"message": "Item not found"},  # Пример ответа
                    "schema": UrlNotFoundResponse.schema(),  # Схема ответа
                }
            },
        }
    },
)
async def delete_url(
    short_url: str,
    shortener_service: Annotated[ShortenerService, Depends(get_shortener_service)],
):
    result = await shortener_service.delete_by_short_code(short_url)
    if result is None:
        raise UrlNotFoundError()


@router.get(
    "/{short_url}/stats",
    response_model=UrlStatsResponse,
    responses={
        404: {
            "description": "Url not found",
            "content": {
                "application/json": {
                    "example": {"message": "Item not found"},  # Пример ответа
                    "schema": UrlNotFoundResponse.schema(),  # Схема ответа
                }
            },
        }
    },
)
async def get_url_stats(
    short_url: str,
    shortener_service: Annotated[ShortenerService, Depends(get_shortener_service)],
):
    result = await shortener_service.get_stats_by_short_code(short_url)
    if result is None:
        raise UrlNotFoundError
    return result
