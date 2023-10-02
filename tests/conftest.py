import asyncio
import sys

import pytest
from httpx import AsyncClient

from main import app, config, db
from main.libs.log import get_logger
from main.models.base import BaseModel
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.utils.auth import create_access_token_from_id

from .helpers import (
    mock_email,
    mock_password,
    prepare_category,
    prepare_item,
    prepare_user,
)

logger = get_logger(__name__)

if config.ENVIRONMENT != "test":
    logger.error('Tests must be run with "ENVIRONMENT=test"')
    sys.exit(1)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop

    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def recreate_database():
    async with db.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest.fixture(scope="function", autouse=True)
async def database():
    connection = await db.engine.connect()
    transaction = await connection.begin()

    db.session_factory.configure(bind=connection)
    db.scoped_session()

    yield

    await db.scoped_session.remove()
    await transaction.rollback()
    await connection.close()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def user():
    return await prepare_user(email=mock_email, password=mock_password)


@pytest.fixture
async def category(user: UserModel):
    return await prepare_category(user.id)


@pytest.fixture
async def item(user: UserModel, category: CategoryModel):
    return await prepare_item(category_id=category.id, creator_id=user.id)


@pytest.fixture
def access_token(user: UserModel):
    return create_access_token_from_id(user.id)
