# Generated by Django 4.1.4 on 2022-12-15 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='description',
            field=models.TextField(default='ghfh'),
            preserve_default=False,
        ),
    ]
