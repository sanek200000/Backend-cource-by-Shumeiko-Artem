from services.auth import AuthService


def test_create_accesse_token():
    data = {"user_id": 1}

    jwt_token = AuthService().create_access_tocken(data)

    assert jwt_token
    assert isinstance(jwt_token, str)
