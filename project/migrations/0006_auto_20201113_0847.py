# Generated by Django 3.1.2 on 2020-11-13 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_restaurant_deliverytime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='average_rating',
            field=models.FloatField(default=3.0),
        ),
    ]