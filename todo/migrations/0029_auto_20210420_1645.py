# Generated by Django 3.1 on 2021-04-20 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0028_auto_20210420_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 20, 16, 45, 30, 577026)),
        ),
        migrations.AlterField(
            model_name='item',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 20, 16, 45, 30, 577026)),
        ),
    ]
