# Generated by Django 3.1 on 2021-04-20 11:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0033_auto_20210420_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 20, 17, 9, 49, 640371)),
        ),
    ]