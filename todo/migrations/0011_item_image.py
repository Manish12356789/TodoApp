# Generated by Django 3.1.7 on 2021-04-08 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_auto_20210407_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='images/'),
        ),
    ]