from datetime import datetime, timedelta
from uuid import uuid4

from jose import jwt
from pytest import fixture

from app.settings import ALGORITHM, SECRET_KEY
from tests.conftest import create_test_auth_headers_for_user


class TestUser:

    async def test_register(self, client: fixture, get_user_from_database):
        data = {
            "username": "ryan_gosling",
            "password": "SampleHashedPass",
            "email": "ryan_gosling@mail.ru",
        }
        response = await client.post("/users/register", json=data)
        assert response.status_code == 200

        data_from_resp = response.json()
        assert data_from_resp["username"] == data["username"]
        assert data_from_resp["email"] == data["email"]

        user_from_db = await get_user_from_database(data_from_resp["id"])
        assert user_from_db is not None
        assert str(user_from_db.id) == data_from_resp["id"]
        assert user_from_db.username == data["username"]
        assert user_from_db.email == data["email"]

    async def test_login(self, client: fixture):
        data = {
            "username": "ryan_gosling",
            "password": "SampleHashedPass",
        }
        response = await client.post("/users/login", data=data)
        assert response.status_code == 200

        # Проверка, что в ответе есть токен
        data_from_resp = response.json()
        assert "access_token" in data_from_resp
        assert "token_type" in data_from_resp
        assert data_from_resp["token_type"] == "bearer"

        # Декодирование токена
        token = data_from_resp["access_token"]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload.get("sub") == "ryan_gosling@mail.ru"

    async def test_get_me(self, client: fixture, get_user_from_database):
        data = {
            "username": "ryan_gosling",
            "password": "SampleHashedPass",
            "email": "ryan_gosling@mail.ru",
        }
        auth_headers = create_test_auth_headers_for_user(data["email"])
        response = await client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200

        data_from_resp = response.json()
        assert data_from_resp["username"] == data["username"]
        assert data_from_resp["email"] == data["email"]

        user_from_db = await get_user_from_database(data_from_resp["id"])
        assert user_from_db is not None
        assert str(user_from_db.id) == data_from_resp["id"]
        assert user_from_db.username == data["username"]
        assert user_from_db.email == data["email"]


class TestReferralCode:

    async def test_create_referral_code(self, client: fixture, get_referral_code_from_database):
        user_data = {
            "email": "ryan_gosling@mail.ru",
        }
        json_body = {'expires_at': (datetime.now() + timedelta(minutes=30)).isoformat()}

        auth_headers = create_test_auth_headers_for_user(user_data["email"])
        response = await client.post("/referral-codes", json=json_body, headers=auth_headers)
        assert response.status_code == 200

        data_from_resp = response.json()
        assert "code" in data_from_resp
        assert data_from_resp["expires_at"] == json_body["expires_at"]

        referral_code_from_db = await get_referral_code_from_database(data_from_resp["code"])
        assert referral_code_from_db is not None
        assert str(referral_code_from_db.id) == data_from_resp["id"]
        assert referral_code_from_db.code == data_from_resp["code"]
        # assert referral_code_from_db.expires_at.isoformat() == data_from_resp["expires_at"]

    async def test_get_referral_code_by_user_email(self, client, get_referral_code_from_database):
        user_data = {
            "email": "ryan_gosling@mail.ru",
        }

        response = await client.get(f"/referral-codes/{user_data['email']}")
        assert response.status_code == 200

        data_from_resp = response.json()
        assert "code" in data_from_resp

        referral_code_from_db = await get_referral_code_from_database(data_from_resp["code"])
        assert referral_code_from_db is not None
        assert referral_code_from_db.code == data_from_resp["code"]

    async def test_delete_referral_code(self, client, get_referral_code_from_database):
        user_data = {
            "email": "ryan_gosling@mail.ru",
        }

        auth_headers = create_test_auth_headers_for_user(user_data["email"])
        response = await client.delete("/referral-codes", headers=auth_headers)
        assert response.status_code == 200

        data_from_resp = response.json()
        assert data_from_resp.get("detail") == "Реферальный код успешно удален."


class TestReferral:

    async def test_get_referrals(self, client, create_user_in_database):
        user_data = {
            "user_id": uuid4(),
            "username": "keanu_reeves",
            "password": "SampleHashedPass!",
            "email": "keanu_reeves@mail.ru",
        }
        await create_user_in_database(**user_data)

        response = await client.get(f"/referrals/{user_data['user_id']}")
        assert response.status_code == 200

        data_from_resp = response.json()

        # Проверяем, что возвращен список (даже если он пуст)
        assert isinstance(data_from_resp, list)
        assert len(data_from_resp) == 0
