import pytest

from db import ASYNC_SESSION_MAKER_NULL_POOL
from utils.db_manager import DBManager


USER_DATA = [
    ("user1", "user1@ya.ru", "111", 200),
    ("user2", "user2@ya.ru", "222", 200),
    ("user3", "user3@ya.ru", "333", 200),
    ("user4", "user4@ya.ru", "444", 200),
    ("user5", "user5@ya.ru", "555", 200),
    (None, None, None, 422),
]


@pytest.fixture(scope="function")
async def test_register_user(ac):
    async def register(name, email, password, status_code):

        response = await ac.post(
            "/auth/register",
            json={
                "name": name,
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == status_code

    return register


@pytest.fixture(scope="function")
async def test_login_user(ac):
    async def login(name, email, password, status_code):

        response = await ac.post(
            url="/auth/login",
            json={
                "name": name,
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == status_code
        if status_code == 200:
            assert ac.cookies.get("access_tocken")
        else:
            assert not ac.cookies.get("access_tocken")

        return ac

    return login


@pytest.fixture(scope="function")
async def test_get_me(ac):
    async def get_me(name, login=True):

        response = await ac.get(url="/auth/me")

        if login:
            assert response.json().get("name") == name
        else:
            assert not response.json().get("name")

    return get_me


@pytest.fixture(scope="function")
async def test_logout(ac):
    async def logout(status_code):

        if status_code == 200:
            response = await ac.post(url="/auth/logout")
            assert response.status_code == status_code

        assert not ac.cookies.get("access_tocken")

    return logout


@pytest.mark.parametrize("name, email, password, status_code", USER_DATA)
async def test_api_auth(
    name,
    email,
    password,
    status_code,
    test_login_user,
    test_register_user,
    test_get_me,
    test_logout,
):

    await test_register_user(name, email, password, status_code)
    await test_login_user(name, email, password, status_code)
    await test_get_me(name)
    await test_logout(status_code)
    await test_get_me(name, login=False)
