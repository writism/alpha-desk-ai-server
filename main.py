from fastapi import FastAPI

from app.domains.stock_normalizer.adapter.inbound.api.normalizer_router import router as normalizer_router
from app.infrastructure.config.settings import Settings, get_settings

settings: Settings = get_settings()

app = FastAPI(debug=settings.debug)

app.include_router(normalizer_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=33333)
