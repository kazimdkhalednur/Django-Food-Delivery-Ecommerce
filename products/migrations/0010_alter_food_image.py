# Generated by Django 4.1.4 on 2023-01-08 14:12

from django.db import migrations, models
import utils.misc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_delete_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.misc.image_path),
        ),
    ]
