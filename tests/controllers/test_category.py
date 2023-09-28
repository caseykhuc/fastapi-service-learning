import pytest

from main.engines.categories import add_category
from main.engines.users import add_user
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.utils.auth import create_access_token_from_id

mock_email = "email@gmail.com"
mock_password = "random_string"


def prepare_user(email: str = mock_email, password: str = mock_password):
    return add_user(email=email, password=password)


def prepare_category(user: UserModel):
    return add_category(name="Cat 1", creator_id=user.id)


@pytest.fixture
async def user():
    return await prepare_user(email=mock_email, password=mock_password)


@pytest.fixture
async def category(user: UserModel):
    return await prepare_category(user)


@pytest.fixture
def access_token(user: UserModel):
    return create_access_token_from_id(user.id)


class TestGetCategories:
    async def test_successfully(self, client, category: CategoryModel):
        response = await client.get("/categories")

        assert response.status_code == 200
        categories = response.json()

        assert len(response.json()) == 1
        assert categories[0]["name"] == category.name


class TestGetCategory:
    async def test_successfully(self, client, category: CategoryModel):
        response = await client.get(f"/categories/{category.id}")

        assert response.status_code == 200
        response_category = response.json()

        assert response_category["name"] == category.name

    async def test_unsuccessfully_not_found(
        self,
        client,
        category: CategoryModel,
    ):
        response = await client.get(f"/categories/{category.id + 1}")

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "payload",
        ["abc", -1, 0],
    )
    async def test_unsuccessfully_validation_error(
        self,
        client,
        payload,
    ):
        response = await client.get(f"/categories/{payload}")

        assert response.status_code == 400


class TestCreateCategory:
    async def test_successfully(self, client, access_token: str):
        response = await client.post(
            "/categories",
            json={"name": "New cat xoxo"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200

    async def test_unsuccessfully_unauthorized(self, client):
        response = await client.post(
            "/categories",
            json={"name": "New cat xoxo"},
        )
        assert response.status_code == 401

    @pytest.mark.parametrize(
        "payload",
        [{}, {"wrong_key": "123"}, {"name": 123}],
    )
    async def test_unsuccessfully_validation_error(
        self,
        client,
        payload,
        access_token,
    ):
        response = await client.post(
            "/categories",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400

    async def test_unsuccessfully_name_exists(
        self,
        client,
        access_token,
        category: CategoryModel,
    ):
        response = await client.post(
            "/categories",
            json={"name": category.name},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400
        assert response.json()["error_code"] == 400002


class TestDeleteCategory:
    async def test_successfully(
        self,
        client,
        access_token: str,
        category: CategoryModel,
    ):
        response = await client.delete(
            f"/categories/{category.id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200

    async def test_unsuccessfully_not_found(
        self,
        client,
        access_token: str,
    ):
        response = await client.delete(
            "/categories/1",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "payload",
        ["abc", -1, 0],
    )
    async def test_unsuccessfully_validation_error(
        self,
        client,
        access_token,
        payload,
    ):
        response = await client.delete(
            f"/categories/{payload}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400

    async def test_unsuccessfully_unauthorized(
        self,
        client,
        category: CategoryModel,
    ):
        response = await client.delete(
            f"/categories/{category.id}",
        )
        assert response.status_code == 401

    async def test_unsuccessfully_not_creator(
        self,
        client,
        category: CategoryModel,
    ):
        user_2 = await prepare_user(email="email2@gmail.com", password=mock_password)
        access_token_2 = create_access_token_from_id(user_2.id)

        response = await client.delete(
            f"/categories/{category.id}",
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        assert response.status_code == 403
