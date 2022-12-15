import time
import os
from django.utils.text import slugify

def generate_slug(title):
    return slugify(title) + "_" + str(int(time.time()))

def image_path(instance, filename):
    return os.path.join(instance.category.title, instance.title,  filename)