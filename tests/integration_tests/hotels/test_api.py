from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


async def test_get_hotels(ac):
    # FastAPICache.init(InMemoryBackend())

    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        },
    )

    assert response.status_code == 200
