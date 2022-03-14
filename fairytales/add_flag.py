from io import BytesIO
from django.core.files import File
from PIL import Image
from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent


def add_flag(image):
    """Adds the image of a flag to an uploaded image."""

    flag_path = os.path.join(BASE_DIR, "static/fairytales/UA2.png")

    flag = Image.open(flag_path)
    flag.convert("RGBA")
    im = Image.open(image)
    im.convert("RGBA")

    image_copy = im.copy()
    position = ((image_copy.width - flag.width), (image_copy.height - flag.height))
    image_copy.paste(flag, position, flag)

    with_flag_io = BytesIO()  # create a BytesIO object

    image_copy.save(with_flag_io, "JPEG", quality=85)  # save image to BytesIO object

    with_flag = File(
        with_flag_io, name=image.name
    )  # create a django friendly File object

    return with_flag
