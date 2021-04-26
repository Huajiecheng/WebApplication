# Generated by Django 3.1.1 on 2020-12-03 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_auto_20201202_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
