from fastapi import FastAPI

from src.shortener.router import router as shortener_router

app = FastAPI(title="UrlShortener")


app.include_router(shortener_router)
