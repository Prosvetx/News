# Generated by Django 3.1.1 on 2020-09-17 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscontent', '0005_auto_20200916_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='valute_name',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='new',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 11, 50, 29, 475327)),
        ),
    ]
