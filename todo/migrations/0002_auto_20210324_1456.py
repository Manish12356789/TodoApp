# Generated by Django 3.1 on 2021-03-24 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='field',
            field=models.CharField(max_length=60),
        ),
    ]
