# Generated by Django 4.1.4 on 2023-01-03 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.CharField(choices=[('2', '2'), ('5', '5'), ('3', '3'), ('1', '1'), ('4', '4')], max_length=5),
        ),
    ]