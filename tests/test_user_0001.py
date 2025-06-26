import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from models import model_user
from utils import security


@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient, async_session: AsyncSession):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Secure@password123",
        "confirm_password": "Secure@password123"
    }

    response = await async_client.post("/user/register", json=user_data)
    response_json = response.json()
    user_uuid = response_json["user_uuid"]
    assert True == isinstance(user_uuid, str)
    assert response.status_code == status.HTTP_201_CREATED
    assert "User successfully registered" in response.text

@pytest.mark.asyncio
async def test_register_user_conflict(async_client: AsyncClient, async_session: AsyncSession):
    user = model_user.User(
        username="duplicateuser",
        email="duplicate@example.com",
        password=security.hash_password("Password@123!"),
        active=True
    )
    async_session.add(user)
    await async_session.commit()

    user_data = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "newpassword",
        "confirm_password": "newpassword"
    }

    response = await async_client.post("/user/register", json=user_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.text


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, async_session: AsyncSession):
    password = "Password@123!"
    user = model_user.User(
        username="loginuser",
        email="login@example.com",
        password=security.hash_password(password),
        active=True
    )
    async_session.add(user)
    await async_session.commit()

    login_data = {
        "email": "login@example.com",
        "password": password,
        "remember": False
    }

    response = await async_client.post("/user/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "Login successful" in response.text
    assert "access_token=" in response.headers.get("set-cookie", "")



@pytest.mark.asyncio
async def test_login_invalid_password(async_client: AsyncClient, async_session: AsyncSession):
    user = model_user.User(
        username="wrongpassuser",
        email="wrongpass@example.com",
        password=security.hash_password("Password@123!"),
        active=True
    )
    async_session.add(user)
    await async_session.commit()

    login_data = {
        "email": "wrongpass@example.com",
        "password": "wrongpassword",
        "remember": False
    }

    response = await async_client.post("/user/login", json=login_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Invalid Credentials" in response.text


@pytest.mark.asyncio
async def test_login_user_not_found(async_client: AsyncClient):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "any-password",
        "remember": False
    }

    response = await async_client.post("/user/login", json=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "User Not Found" in response.text


@pytest.mark.asyncio
async def test_login_user_inactive(async_client: AsyncClient, async_session: AsyncSession):
    user = model_user.User(
        username="inactiveuser",
        email="inactive@example.com",
        password=security.hash_password("Password@123!"),
        active=False
    )
    async_session.add(user)
    await async_session.commit()

    login_data = {
        "email": "inactive@example.com",
        "password": "Password@123!",
        "remember": False
    }

    response = await async_client.post("/user/login", json=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Inactive" in response.text
