# Generated by Django 3.1 on 2021-04-20 08:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0020_auto_20210420_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.localtime),
        ),
    ]