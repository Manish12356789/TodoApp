# Generated by Django 3.1 on 2021-04-22 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0037_remove_item_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(default=True, max_length=50),
        ),
    ]