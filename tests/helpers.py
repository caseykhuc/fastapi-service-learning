import random
import string
from datetime import datetime

from main.engines.categories import add_category
from main.engines.items import add_item
from main.engines.users import add_user

mock_email = "email@gmail.com"
mock_password = "random_string"


def prepare_user(email: str = mock_email, password: str = mock_password):
    return add_user(email=email, password=password)


def prepare_category(creator_id: int):
    return add_category(
        name="Cat 1",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
        creator_id=creator_id,
    )


def prepare_item(category_id: int, creator_id: int):
    return add_item(
        name="Item 1",
        description="mock description",
        category_id=category_id,
        creator_id=creator_id,
    )


def generate_random_string(length: int = 255):
    return "".join(
        # ruff: noqa: S311
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )


async def prepare_bulk_items(category_id: int, creator_id: int, count: int = 1):
    key = datetime.now()
    for i in range(count):
        await add_item(
            name=f"Mock item - {key} - {i}",
            description="Mock description",
            creator_id=creator_id,
            category_id=category_id,
        )
