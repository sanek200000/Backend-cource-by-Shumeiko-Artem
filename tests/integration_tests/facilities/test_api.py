from fastapi_cache.backends.inmemory import InMemoryBackend


async def test_get_ficilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_ficilities(ac):
    facility_title = "Массаж"
    response = await ac.post("/facilities", json={"title": facility_title})

    res = response.json()
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert "data" in res
    assert res.get("data").get("title") == facility_title
