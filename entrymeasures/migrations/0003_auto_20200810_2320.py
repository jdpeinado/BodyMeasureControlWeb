# Generated by Django 3.0.7 on 2020-08-10 23:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrymeasures', '0002_auto_20200810_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrymeasure',
            name='date_measure',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
    ]