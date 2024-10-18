from datetime import datetime, timedelta
from uuid import uuid4

from pytest import fixture

from tests.conftest import create_test_auth_headers_for_user


class TestUser:

    async def test_register(self, client: fixture):
        json = {
            "username": "ryan_gosling",
            "password": "SamplePass1!",
            "email": "ryan_gosling@mail.ru",
        }
        response = await client.post("/users/register", json=json)
        assert response.status_code == 200

    async def test_login(self, client: fixture):
        user_data = {
            "username": "ryan_gosling",
            "password": "SamplePass1!",
        }
        response = await client.post("/users/login", data=user_data)
        assert response.status_code == 200

    async def test_me(self, client: fixture):
        user_data = {
            "username": "ryan_gosling",
            "password": "SamplePass1!",
            "email": "ryan_gosling@mail.ru",
        }
        response = await client.get(
            "/users/me",
            headers=create_test_auth_headers_for_user(user_data["email"])
        )
        assert response.status_code == 200


class TestReferralCode:

    async def test_create(self, client: fixture):
        user_data = {
            "username": "ryan_gosling",
            "password": "SamplePass1!",
            "email": "ryan_gosling@mail.ru",
        }
        json = {'expires_at': str(datetime.now() + timedelta(minutes=30))}
        response = await client.post(
            "/referral-codes", json=json,
            headers=create_test_auth_headers_for_user(user_data["email"])
        )
        assert response.status_code == 200

    async def test_get(self, client):
        user_data = {
            "username": "ryan_gosling",
            "password": "SamplePass1!",
            "email": "ryan_gosling@mail.ru",
        }
        response = await client.get(
            f"/referral-codes/{user_data['email']}",
            headers=create_test_auth_headers_for_user(user_data['email'])
        )
        assert response.status_code == 200

    async def test_delete(self, client):
        user_data = {
            "username": "ryan_gosling",
            "password": "SamplePass1!",
            "email": "ryan_gosling@mail.ru",
        }
        response = await client.delete(
            "/referral-codes",
            headers=create_test_auth_headers_for_user(user_data['email'])
        )
        assert response.status_code == 200


class TestReferral:

    async def test_get_all(self, client, create_user_in_database):
        user_data = {
            "user_id": uuid4(),
            "username": "keanu_reeves",
            "password": "SampleHashedPass!",
            "email": "keanu_reeves@mail.ru",
        }
        await create_user_in_database(**user_data)

        response = await client.get(f"/referrals/{user_data['user_id']}")
        assert response.status_code == 200
