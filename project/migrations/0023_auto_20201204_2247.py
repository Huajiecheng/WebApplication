# Generated by Django 3.1.1 on 2020-12-04 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0022_auto_20201204_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='location',
            field=models.CharField(default='', max_length=200),
        ),
    ]
