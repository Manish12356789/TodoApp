# Generated by Django 3.1 on 2021-04-20 07:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0019_auto_20210420_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
