import os
from time import sleep
from PIL import Image

from tasks.celery_app import celery_instance


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
