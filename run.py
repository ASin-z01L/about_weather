from fastapi import FastAPI
from fastapi import APIRouter
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import logging
from app.routers import weather


@asynccontextmanager
async def lifespan(_: FastAPI):
    load_dotenv('.env')

    logging.basicConfig(
        level=logging.ERROR,
        filename='app.log',
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    yield


app = FastAPI(lifespan=lifespan)
router = APIRouter()

app.include_router(weather.router)

if __name__ == "__main__":
    uvicorn.run("run:app", reload=True)
