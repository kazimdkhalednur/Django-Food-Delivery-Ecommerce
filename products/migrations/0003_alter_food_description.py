# Generated by Django 4.1.4 on 2022-12-15 21:54

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_food_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
