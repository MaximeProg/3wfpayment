from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

# statement_cache_size=0 : le endpoint "pooled" de Neon (PgBouncer, mode transaction)
# n'est pas compatible avec les prepared statements mis en cache par asyncpg.
engine = create_async_engine(
    settings.database_url,
    connect_args={"ssl": "require", "statement_cache_size": 0},
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
