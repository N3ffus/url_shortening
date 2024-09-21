from typing import Annotated

from fastapi import Depends

from src.services.shortener_service import ShortenerService
from src.utils.unitofwork import AbstractUnitOfWork, UnitOfWork

ALLOWED = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
LENGTH = len(ALLOWED)  # length of ALLOWED (62)


async def get_shortener_service(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
) -> ShortenerService:
    return ShortenerService(uow)


class Shortener:
    @classmethod
    async def create_url(cls, shortener_service: ShortenerService):
        number = await shortener_service.get_count() + 1
        return cls.__number_to_string(number)

    @staticmethod
    def __number_to_string(number):
        if number == 0:
            return ALLOWED[0]
        tmp = []
        while number > 0:
            tmp.append(number % LENGTH)
            number //= LENGTH
        result = [ALLOWED[index] for index in reversed(tmp)]
        return "".join(result)
