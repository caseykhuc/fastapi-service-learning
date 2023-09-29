import pytest

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
