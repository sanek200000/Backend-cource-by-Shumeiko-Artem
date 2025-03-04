import pytest

from db import ASYNC_SESSION_MAKER_NULL_POOL
from utils.db_manager import DBManager


@pytest.fixture(scope="module")
async def delete_all_bookings():

    async with DBManager(ASYNC_SESSION_MAKER_NULL_POOL) as db_:
        await db_.bookings.delete()
        await db_.commit()

        response = await db_.bookings.get_all()

    assert response == []


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-02", "2024-08-11", 200),
        (1, "2024-08-03", "2024-08-12", 200),
        (1, "2024-08-04", "2024-08-13", 200),
        (1, "2024-08-05", "2024-08-14", 200),
        (1, "2024-08-06", "2024-08-15", 409),
        (1, "2024-08-11", "2024-08-14", 200),
    ],
)
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    authenticated_ac,
):

    # room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res.get("status") == "OK"
        assert "data" in res


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, count",
    [
        (1, "2024-08-01", "2024-08-10", 200, 1),
        (1, "2024-08-01", "2024-08-10", 200, 2),
        (1, "2024-08-01", "2024-08-10", 200, 3),
        (1, "2024-08-01", "2024-08-10", 200, 4),
        (1, "2024-08-01", "2024-08-10", 200, 5),
    ],
)
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    status_code,
    count,
    delete_all_bookings,
    authenticated_ac,
):

    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if status_code == 200:
        response = await authenticated_ac.get("/bookings/me")
        res: list = response.json()
        assert len(res) == count
