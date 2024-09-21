from src.shortener.schemas import UrlResponse, UrlStatsResponse
from src.utils.unitofwork import AbstractUnitOfWork


class ShortenerService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def add_url(self, short_url: str, url: str) -> UrlResponse:
        url_dict: dict = {"short_code": short_url, "url": url}

        async with self.uow:
            url_from_db = await self.uow.shortener.add_one(url_dict)
            url_scheme = UrlResponse.model_validate(url_from_db)
            await self.uow.commit()

            return url_scheme

    async def get_all_urls(self) -> list[UrlResponse]:
        async with self.uow:
            urls = await self.uow.shortener.get_all()
            return [UrlResponse.model_validate(url) for url in urls]

    async def get_count(self) -> int:
        async with self.uow:
            count: int = await self.uow.shortener.get_count()
            return count

    async def get_url_by_short_code(self, short_code: str):
        async with self.uow:
            result = await self.uow.shortener.get_url_by_short_code(short_code)
            if result is None:
                return None
            url_response = UrlResponse.model_validate(result)
            return url_response

    async def get_url(self, url: str):
        async with self.uow:
            result = await self.uow.shortener.get_url(url)
            if result is None:
                return None
            url_response = UrlResponse.model_validate(result)
            return url_response

    async def update_by_short_code(self, short_code: str, new_url: str):
        async with self.uow:
            result = await self.uow.shortener.update_url_by_short_code(
                short_code, new_url
            )
            if result is None:
                return None
            url_response = UrlResponse.model_validate(result)
            await self.uow.commit()
            return url_response

    async def delete_by_short_code(self, short_code: str):
        async with self.uow:
            result = await self.uow.shortener.delete_by_short_code(short_code)
            if result is None:
                return None
            await self.uow.commit()
            return True

    async def get_stats_by_short_code(self, short_code: str):
        async with self.uow:
            result = await self.uow.shortener.get_url_by_short_code(short_code)
            if result is None:
                return None
            return UrlStatsResponse.model_validate(result)

    async def increment_by_short_code(self, short_code: str, value: int):
        async with self.uow:
            result = await self.uow.shortener.increment_by_short_code(short_code, value)
            await self.uow.commit()
            if result is None:
                return None
            return True
