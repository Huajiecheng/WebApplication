# Generated by Django 3.1.1 on 2020-11-17 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_auto_20201116_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='instruction',
            field=models.CharField(default='', max_length=200),
        ),
    ]