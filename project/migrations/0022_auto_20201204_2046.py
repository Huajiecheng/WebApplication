# Generated by Django 3.1.2 on 2020-12-04 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_auto_20201204_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressprofile',
            name='postal_code',
            field=models.CharField(default='', max_length=5),
        ),
    ]
