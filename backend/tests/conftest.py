import os

import pytest

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_blehub.db"

from app.db.models import Base
from app.db.session import engine


@pytest.fixture(autouse=True)
async def reset_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield
