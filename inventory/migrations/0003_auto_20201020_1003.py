# Generated by Django 3.1.1 on 2020-10-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20201020_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='productId',
            field=models.IntegerField(default=0),
        ),
    ]
