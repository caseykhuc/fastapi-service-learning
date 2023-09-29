import random
import string

from main.engines.categories import add_category
from main.engines.items import add_item
from main.engines.users import add_user

mock_email = "email@gmail.com"
mock_password = "random_string"


def prepare_user(email: str = mock_email, password: str = mock_password):
    return add_user(email=email, password=password)


def prepare_category(user_id: int):
    return add_category(name="Cat 1", creator_id=user_id)


def prepare_item(category_id: int, user_id: int):
    return add_item(
        name="Item 1",
        description="mock description",
        category_id=category_id,
        creator_id=user_id,
    )


def generate_random_string(length: int = 255):
    return "".join(
        # ruff: noqa: S311
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )
