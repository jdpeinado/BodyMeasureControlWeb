# Generated by Django 3.0.7 on 2020-06-22 16:33

from django.db import migrations
import django_measurement.models
import measurement.measures.distance
import measurement.measures.mass


class Migration(migrations.Migration):

    dependencies = [
        ('entrymeasures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrymeasure',
            name='bicep',
            field=django_measurement.models.MeasurementField(measurement=measurement.measures.distance.Distance),
        ),
        migrations.AlterField(
            model_name='entrymeasure',
            name='bodyweight',
            field=django_measurement.models.MeasurementField(measurement=measurement.measures.mass.Mass),
        ),
        migrations.AlterField(
            model_name='entrymeasure',
            name='chest',
            field=django_measurement.models.MeasurementField(measurement=measurement.measures.distance.Distance),
        ),
        migrations.AlterField(
            model_name='entrymeasure',
            name='hip',
            field=django_measurement.models.MeasurementField(measurement=measurement.measures.distance.Distance),
        ),
        migrations.AlterField(
            model_name='entrymeasure',
            name='leg',
            field=django_measurement.models.MeasurementField(measurement=measurement.measures.distance.Distance),
        ),
        migrations.AlterField(
            model_name='entrymeasure',
            name='waist',
            field=django_measurement.models.MeasurementField(measurement=measurement.measures.distance.Distance),
        ),
    ]
