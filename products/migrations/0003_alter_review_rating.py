# Generated by Django 4.1.4 on 2023-01-03 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.CharField(choices=[('1', '1'), ('5', '5'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=5),
        ),
    ]
