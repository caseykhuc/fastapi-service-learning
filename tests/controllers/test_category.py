import pytest

from main.models.category import CategoryModel
from main.utils.auth import create_access_token_from_id
from tests.helpers import generate_random_string, mock_password, prepare_user


class TestGetCategories:
    async def test_successfully(self, client, category: CategoryModel):
        response = await client.get("/categories")

        assert response.status_code == 200
        categories = response.json()

        assert len(categories) == 1
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
            json={"name": generate_random_string(255)},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200

    async def test_unsuccessfully_unauthorized(self, client):
        response = await client.post(
            "/categories",
            json={"name": "New category"},
        )
        assert response.status_code == 401

    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"wrong_key": "123"},
            {"name": 123},
            {"name": generate_random_string(256)},
        ],
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
