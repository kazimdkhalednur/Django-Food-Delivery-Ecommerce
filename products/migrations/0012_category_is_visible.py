# Generated by Django 4.1.4 on 2023-01-08 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
    ]
