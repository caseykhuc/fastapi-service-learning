from urllib import parse

import pytest

from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.utils.auth import create_access_token_from_id
from tests.helpers import (
    generate_random_string,
    mock_password,
    prepare_bulk_items,
    prepare_user,
)


class TestGetCategoryItems:
    async def test_successfully(self, client, category: CategoryModel, item: ItemModel):
        response = await client.get(f"/categories/{category.id}/items")

        assert response.status_code == 200
        data = response.json()

        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == item.name

    async def test_successfully_with_pagination(
        self,
        client,
        user,
        category: CategoryModel,
    ):
        total_items = 25
        await prepare_bulk_items(
            category_id=category.id,
            creator_id=user.id,
            count=total_items,
        )

        async def _test(
            assert_len: int,
            page: int | None = None,
            number_per_page: int | None = None,
        ):
            query_config = {}
            if page:
                query_config["page"] = page
            if number_per_page:
                query_config["number_per_page"] = number_per_page
            response = await client.get(
                f"/categories/{category.id}/items?{parse.urlencode(query_config)}",
            )
            assert response.status_code == 200
            data = response.json()

            assert len(data["items"]) == assert_len
            assert data["total"] == total_items

        await _test(page=1, assert_len=20)
        await _test(page=2, assert_len=5)
        await _test(page=3, assert_len=0)
        await _test(page=2, number_per_page=15, assert_len=10)

    async def test_unsuccessfully_not_found(
        self,
        client,
        category: CategoryModel,
    ):
        response = await client.get(f"/categories/{category.id + 1}/items")

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "payload",
        ["abc", -1, 0],
    )
    async def test_unsuccessfully_path_validation_error(
        self,
        client,
        payload,
    ):
        response = await client.get(f"/categories/{payload}/items")

        assert response.status_code == 400

    @pytest.mark.parametrize(
        "query",
        ["page=0", "page=-1", "page=abc"],
    )
    async def test_unsuccessfully_query_validation_error(
        self,
        client,
        query,
        category: CategoryModel,
    ):
        response = await client.get(f"/categories/{category.id}/items?{query}")

        assert response.status_code == 400


class TestGetItemDetails:
    async def test_successfully(self, client, item: ItemModel):
        response = await client.get(f"/items/{item.id}")

        assert response.status_code == 200
        response_item = response.json()
        assert response_item["name"] == item.name
        assert response_item["description"] == item.description

    async def test_unsuccessfully_not_found(self, client, item: ItemModel):
        response = await client.get(f"/items/{item.id +1}")

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
        response = await client.get(f"/items/{payload}")

        assert response.status_code == 400


class TestCreateItem:
    async def test_successfully(
        self,
        client,
        category: CategoryModel,
        access_token: str,
    ):
        response = await client.post(
            f"/categories/{category.id}/items",
            json={
                "name": generate_random_string(255),
                "description": generate_random_string(5000),
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200

    async def test_unsuccessfully_unauthorized(self, category: CategoryModel, client):
        response = await client.post(
            f"/categories/{category.id}/items",
            json={"name": "New item"},
        )
        assert response.status_code == 401

    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"wrong_key": "123"},
            {"name": 123, "description": ""},
            {"name": generate_random_string(256), "description": "mock description"},
            {"name": generate_random_string(255), "description": ""},
            {
                "name": generate_random_string(255),
                "description": generate_random_string(5001),
            },
        ],
    )
    async def test_unsuccessfully_validation_error(
        self,
        client,
        payload,
        access_token,
        category: CategoryModel,
    ):
        response = await client.post(
            f"/categories/{category.id}/items",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400

    async def test_unsuccessfully_name_exists(
        self,
        client,
        access_token,
        category: CategoryModel,
        item: ItemModel,
    ):
        response = await client.post(
            f"/categories/{category.id}/items",
            json={"name": item.name, "description": "mock description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400
        assert response.json()["error_code"] == 400004


class TestUpdateItem:
    new_name = generate_random_string(255)
    new_description = generate_random_string(5000)

    async def test_successfully(
        self,
        client,
        access_token: str,
        item: ItemModel,
    ):
        response = await client.put(
            f"/items/{item.id}",
            json={"name": self.new_name, "description": self.new_description},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

        response_item = response.json()
        assert response_item["name"] == self.new_name
        assert response_item["description"] == self.new_description

    async def test_unsuccessfully_not_found(
        self,
        client,
        access_token: str,
        item: ItemModel,
    ):
        response = await client.put(
            f"/items/{item.id + 1}",
            json={"name": self.new_name, "description": self.new_description},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"wrong_key": "123"},
            {"name": 123},
            {"name": ""},
            {"name": generate_random_string(256)},
            {"description": ""},
            {"description": generate_random_string(5001)},
        ],
    )
    async def test_unsuccessfully_validation_error(
        self,
        client,
        access_token,
        payload,
        item,
    ):
        response = await client.put(
            f"/items/{item.id}",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400

    async def test_unsuccessfully_unauthorized(
        self,
        client,
        item: ItemModel,
    ):
        response = await client.put(
            f"/items/{item.id}",
        )
        assert response.status_code == 401

    async def test_unsuccessfully_not_creator(
        self,
        client,
        item: ItemModel,
    ):
        user_2 = await prepare_user(email="email2@gmail.com", password=mock_password)
        access_token_2 = create_access_token_from_id(user_2.id)

        response = await client.put(
            f"/items/{item.id}",
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        assert response.status_code == 403


class TestDeleteItem:
    async def test_successfully(
        self,
        client,
        access_token: str,
        item: ItemModel,
    ):
        response = await client.delete(
            f"/items/{item.id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200

    async def test_unsuccessfully_not_found(
        self,
        client,
        access_token: str,
        item: ItemModel,
    ):
        response = await client.delete(
            f"/items/{item.id + 1}",
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
            f"/items/{payload}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400

    async def test_unsuccessfully_unauthorized(
        self,
        client,
        item: ItemModel,
    ):
        response = await client.delete(
            f"/items/{item.id}",
        )
        assert response.status_code == 401

    async def test_unsuccessfully_not_creator(
        self,
        client,
        item: ItemModel,
    ):
        user_2 = await prepare_user(email="email2@gmail.com", password=mock_password)
        access_token_2 = create_access_token_from_id(user_2.id)

        response = await client.delete(
            f"/items/{item.id}",
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        assert response.status_code == 403
