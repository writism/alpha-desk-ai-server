from fastapi import FastAPI

from app.infrastructure.config.settings import Settings, get_settings

settings: Settings = get_settings()

app = FastAPI(debug=settings.debug)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=33333)
