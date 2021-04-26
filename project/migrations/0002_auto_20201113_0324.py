# Generated by Django 3.1.2 on 2020-11-13 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='location',
            field=models.CharField(default='', max_length=200),
        ),
    ]
