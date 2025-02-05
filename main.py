from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
import uvicorn

from src.db.session import engine, Base
from src.routes.server import servers_router
from src.core.worker import celery_app
from src.tasks.get_servers import get_active_servers


async def check_servers():
    get_active_servers.delay()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    
    scheduler = AsyncIOScheduler()
    # repeat task every 10 seconds
    scheduler.add_job(func=check_servers, trigger='interval', seconds=5)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(servers_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
