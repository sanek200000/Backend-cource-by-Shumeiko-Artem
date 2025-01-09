from typing import Any


class AuthOE:

    register = {
        "1": {
            "summary": "user1",
            "value": {
                "name": "user1",
                "email": "user1@example.com",
                "password": "password",
            },
        },
        "2": {
            "summary": "user2",
            "value": {
                "name": "user2",
                "email": "user2@example.com",
                "password": "password",
            },
        },
        "3": {
            "summary": "user3",
            "value": {
                "name": "user3",
                "email": "user3@example.com",
                "password": "password",
            },
        },
    }

    login = {
        "1": {
            "summary": "user1",
            "value": {
                "name": "user1",
                "email": "user1@example.com",
                "password": "password",
            },
        },
        "2": {
            "summary": "user2",
            "value": {
                "name": "user2",
                "email": "user2@example.com",
                "password": "password",
            },
        },
        "3": {
            "summary": "user3",
            "value": {
                "name": "user3",
                "email": "user3@example.com",
                "password": "password",
            },
        },
    }


class BookingOE:

    create = {
        "1": {
            "summary": "Бронирование1",
            "value": {
                "room_id": 1,
                "date_from": "2025-11-01",
                "date_to": "2025-11-10",
            },
        },
        "2": {
            "summary": "Бронирование2",
            "value": {
                "room_id": 1,
                "date_from": "2025-10-25",
                "date_to": "2025-11-05",
            },
        },
        "3": {
            "summary": "Бронирование3",
            "value": {
                "room_id": 1,
                "date_from": "2025-11-09",
                "date_to": "2025-11-20",
            },
        },
    }


class FacilitiesOE:

    create = {
        "1": {
            "summary": "Internet",
            "value": {
                "title": "WiFi",
            },
        },
        "2": {
            "summary": "Жакузя",
            "value": {
                "title": "Жакузя",
            },
        },
        "3": {
            "summary": "Туалет",
            "value": {
                "title": "Туалет",
            },
        },
    }


class HotelsOE:

    create = {
        "1": {
            "summary": "Сочи1",
            "value": {
                "title": "Атрия",
                "location": "Адлерский район, улица Мира, д.44 а, Сочи",
            },
        },
        "2": {
            "summary": "Сочи2",
            "value": {
                "title": "Радуга-Престиж",
                "location": "Краснодарский край, г. Сочи, ул. Пирогова, д. 2/3",
            },
        },
        "3": {
            "summary": "Дубай1",
            "value": {
                "title": "Отель Al Khoory Executive Hotel",
                "location": "Al Wasl Area, Dubai, Дубай",
            },
        },
        "4": {
            "summary": "Дубай2",
            "value": {
                "title": "Holiday Inn Express Dubai Internet City an IHG Hotel",
                "location": "Knowledge Village Pob 282647, Дубай",
            },
        },
    }


class RoomsOE:

    create = {
        "1": {
            "summary": "standart",
            "value": {
                "hotel_id": 0,
                "title": "standart",
                "description": "sfsdfsdf sdfsdf sdfsdf sdfsdf",
                "price": 10,
                "quantity": 10,
                "facilities_ids": [1, 2],
            },
        },
        "2": {
            "summary": "comfort",
            "value": {
                "hotel_id": 0,
                "title": "comfort",
                "description": "sfsdfsdf sdfsdf sdfsdf sdfsdf",
                "price": 100,
                "quantity": 5,
                "facilities_ids": [2, 3],
            },
        },
        "3": {
            "summary": "luxe",
            "value": {
                "hotel_id": 0,
                "title": "luxe",
                "description": "sfsdfsdf sdfsdf sdfsdf sdfsdf",
                "price": 1000,
                "quantity": 1,
                "facilities_ids": [1, 3],
            },
        },
    }
