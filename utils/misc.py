import time
import os
from django.utils.text import slugify


def generate_slug(title):
    return slugify(title) + "_" + str(int(time.time()))


def image_path(instance, filename):
    return os.path.join(instance.category.title, instance.title,  filename)


def image_path_category(instance, filename):
    return os.path.join(instance.title,  filename)


def profile_image_path(instance, filename):
    return os.path.join(instance.email,  filename)
