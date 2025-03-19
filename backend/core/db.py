from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr, Mapped
from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyPlugin, base

DATABASE_URL = "sqlite+aiosqlite:///blog.db"

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite", session_config=session_config, create_all=True
) 

class PreBase:
    """
    Mixin for Base models, include id and defining name of model.
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    id: Mapped[int] = Column(Integer, primary_key=True)

Base = declarative_base(cls=PreBase)

async def get_db_session():
    """Dependency for database session."""
    async with async_session_factory() as session:
        yield session



