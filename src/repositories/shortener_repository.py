from sqlalchemy import delete, select, update

from src.repositories.base_repository import Repository
from src.shortener.models import Url


class ShortenerRepository(Repository):
    model = Url

    async def get_url_by_short_code(self, short_code: str):
        stmt = select(Url).where(Url.short_code == short_code)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_url(self, url: str):
        stmt = select(Url).where(Url.url == url)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def update_url_by_short_code(self, short_code: str, new_url: str):
        stmt = (
            update(Url)
            .where(Url.short_code == short_code)
            .values(url=new_url)
            .returning(Url)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def delete_by_short_code(self, short_code: str):
        stmt = delete(Url).where(Url.short_code == short_code).returning(Url)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def increment_by_short_code(self, short_code: str, value: int):
        stmt = (
            update(Url)
            .where(Url.short_code == short_code)
            .values(access_count=Url.access_count + value)
            .returning(Url)
        )
        result = await self.session.execute(stmt)
        return result.scalar()
