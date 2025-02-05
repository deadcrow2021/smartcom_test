from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

from src.core.settings import db_settings

Base = declarative_base()

engine = create_engine(
    url=db_settings.db_url,
    echo=db_settings.db_debug,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True
)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

def get_session():
    session = Session()
    return session

    # try:
    #     yield session
    # finally:
    #     session.close()
