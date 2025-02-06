from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


async def test_get_hotels(ac):

    response = await ac.get("/facilities")
    print(f"=================== {response.json() = } ===========================")

    assert response.status_code == 200
