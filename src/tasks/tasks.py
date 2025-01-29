import asyncio
import os
from time import sleep
from PIL import Image

from api import bookings
from db import ASYNC_SESSION_MAKER_NULL_POOL
from tasks.celery_app import celery_instance
from utils.db_manager import DBManager


@celery_instance.task
def test_task():
    # Run task `celery --app=tasks.celery_app:celery_instance worker -l INFO`
    sleep(5)
    print("я молодец")


@celery_instance.task
def resize_image(input_image_path: str):
    output_directory = "static/images/"
    widths = [1000, 500, 200]

    # Открываем исходное изображение
    with Image.open(input_image_path) as image:
        original_width, original_height = image.size
        aspect_ratio = original_height / original_width

        for width in widths:
            # Вычисляем новую высоту с сохранением пропорций
            new_height = int(width * aspect_ratio)
            resized_image = image.resize((width, new_height), Image.LANCZOS)

            # Формируем имя файла и сохраняем изображение
            output_path = os.path.join(output_directory, f"image_{width}.jpg")
            resized_image.save(output_path)
            print(f"Изображение сохранено: {output_path}")


async def get_bookings_with_today_chechin_helper():
    print("я `get_bookings_with_today_chechin_helper` запускаюсь")
    async with DBManager(session_factory=ASYNC_SESSION_MAKER_NULL_POOL) as db:
        bookings = await db.bookings.get_bookings_with_today_checin()
        print(f"{bookings}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_chechin_helper())
