from services.auth import AuthService


def test_create_accesse_token():
    data = {"user_id": 1}

    jwt_token = AuthService().create_access_tocken(data)

    payload = AuthService().decode_token(jwt_token)
    assert payload
    assert payload["user_id"] == data["user_id"]
