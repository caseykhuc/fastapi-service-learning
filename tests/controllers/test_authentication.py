import pytest

from main.engines.users import add_user


async def test_sign_up_successfully(client):
    response = await client.post(
        "/register",
        json={"email": "email@gmail.com", "password": "1234aA"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"email": "not_an_email"},
        {"password": "1234"},
        {"email": "email@gmail.com"},
        {"password": "1234@Ab"},
        {"email": "email@gmail.com", "password": "12@Ab"},
        {"email": "email@gmail.com", "password": "123456"},
        {"email": "email@gmail.com", "password": "12345a"},
    ],
)
async def test_sign_up_unsuccessfully_with_validation_error(client, payload):
    response = await client.post("/register", json=payload)
    assert response.status_code == 400


async def test_sign_up_unsuccessfully_with_existing_email(client):
    email = "email@gmail.com"
    password = "test_password"
    await add_user(email=email, password=password)

    response = await client.post(
        "/register",
        json={"email": email, "password": "1234aA"},
    )
    assert response.status_code == 400


async def test_login_succesfully(client):
    email = "email@gmail.com"
    password = "test_password"
    await add_user(email=email, password=password)

    response = await client.post(
        "/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"email": "not_an_email"},
        {"password": "1234"},
        {"email": "email@gmail.com"},
        {"password": "1234@Ab"},
    ],
)
async def test_login_unsuccessfully_with_validation_error(client, payload):
    response = await client.post("/login", json=payload)
    assert response.status_code == 400


async def test_login_unsuccessfully_with_unmatched_credentials(client):
    email = "email@gmail.com"
    password = "test_password"
    await add_user(email=email, password=password)

    response = await client.post(
        "/login",
        json={"email": email, "password": "other_password"},
    )
    assert response.status_code == 401
