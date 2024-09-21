import pytest
from httpx import AsyncClient

from src.services.shortener_service import ShortenerService
from src.shortener.utils import Shortener


@pytest.mark.asyncio
async def test_create_short_url(ac: AsyncClient):
    response = await ac.post(
        "/shorten/",
        json={
            "url": "https://www.example.com/",
        },
    )

    assert response.status_code == 201
    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["short_code"] == "b"
    assert response_json["url"] == "https://www.example.com/"


@pytest.mark.asyncio
async def test_shortener(shortener_service: ShortenerService):
    result = await Shortener.create_url(shortener_service)

    assert result == "b"


@pytest.mark.asyncio
async def test_get_original_url(ac: AsyncClient, shortener_service: ShortenerService):
    response = await ac.get("/shorten/b")

    assert response.status_code == 404

    await shortener_service.add_url("abcde", "https://www.example.com/")
    response = await ac.get("/shorten/abcde")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == 1
    assert response_json["short_code"] == "abcde"
    assert response_json["url"] == "https://www.example.com/"


@pytest.mark.asyncio
async def test_update_url(ac: AsyncClient, shortener_service: ShortenerService):
    response = await ac.put("/shorten/b", json={"url": "https://www.example.com/"})

    assert response.status_code == 404
    await shortener_service.add_url("abcde", "https://www.example.com/")

    response = await ac.put(
        "/shorten/abcde", json={"url": "https://www.newexample.com/"}
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == 1
    assert response_json["short_code"] == "abcde"
    assert response_json["url"] == "https://www.newexample.com/"


@pytest.mark.asyncio
async def test_delete_url(ac: AsyncClient, shortener_service: ShortenerService):
    response = await ac.delete("/shorten/b")

    assert response.status_code == 404

    await shortener_service.add_url("abcde", "https://www.example.com/")
    response = await ac.delete("/shorten/abcde")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_url_stats(ac: AsyncClient, shortener_service: ShortenerService):
    response = await ac.get("/shorten/b/stats")

    assert response.status_code == 404

    await shortener_service.add_url("abcde", "https://www.example.com/")
    response = await ac.get("/shorten/abcde/stats")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == 1
    assert response_json["short_code"] == "abcde"
    assert response_json["url"] == "https://www.example.com/"
    assert response_json["access_count"] == 0

    for i in range(10):
        await ac.get("/shorten/abcde")

    response = await ac.get("/shorten/abcde/stats")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == 1
    assert response_json["short_code"] == "abcde"
    assert response_json["url"] == "https://www.example.com/"
    assert response_json["access_count"] == 10
