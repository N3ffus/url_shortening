from typing import Annotated

import pytest
import pytest_asyncio
from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.config import settings
from src.database import Base
from src.main import app
from src.services.shortener_service import ShortenerService
from src.shortener.utils import get_shortener_service
from src.utils.unitofwork import AbstractUnitOfWork, UnitOfWork


class TestUnitOfWork(UnitOfWork):
    def __init__(self):
        super().__init__()
        self.session_factory = async_sessionmaker(
            create_async_engine(settings.TEST_DATABASE_URL),
            class_=AsyncSession,
            expire_on_commit=False,
        )


async def get_test_shortener_service() -> ShortenerService:
    return ShortenerService(TestUnitOfWork())


app.dependency_overrides[get_shortener_service] = get_test_shortener_service


@pytest_asyncio.fixture(scope="function")
async def ac():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    engine = create_async_engine(settings.TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function")
async def shortener_service():
    return ShortenerService(TestUnitOfWork())
