# Generated by Django 3.1.2 on 2020-12-01 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_auto_20201201_0714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewimage',
            name='review',
        ),
        migrations.AddField(
            model_name='review',
            name='images',
            field=models.ManyToManyField(to='project.ReviewImage'),
        ),
    ]
