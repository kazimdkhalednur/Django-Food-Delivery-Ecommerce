# Generated by Django 4.1.4 on 2023-01-08 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_alter_cart_rating_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='rating',
            field=models.CharField(blank=True, choices=[('4', '4'), ('5', '5'), ('1', '1'), ('3', '3'), ('2', '2')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('stolen', 'Stolen'), ('paid', 'Paid'), ('on_the_way', 'On The Way'), ('delivered', 'Delivered'), ('pending', 'Pending')], max_length=20),
        ),
    ]
