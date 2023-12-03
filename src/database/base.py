from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from src.settings import DATABASE_URL_ASYNC, DATABASE_URL_SYNC

# Sync
engin_sync = create_engine(DATABASE_URL_SYNC)
sync_session = sessionmaker(engin_sync)

# Async
engine_async = create_async_engine(DATABASE_URL_ASYNC)
async_session = async_sessionmaker(engine_async, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
