# Generated by Django 2.2.16 on 2020-09-07 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raceratings', '0011_exportrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exportrecord',
            name='record_type',
            field=models.SlugField(choices=[('cumulative-records', 'Cumulative winner records'), ('race-ratings', 'Race ratings'), ('rating-deltas', 'Race rating deltas')], default='cumulative-records', max_length=25),
        ),
    ]
