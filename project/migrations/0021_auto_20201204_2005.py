# Generated by Django 3.1.2 on 2020-12-04 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_auto_20201203_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressprofile',
            name='content_type',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='addressprofile',
            name='picture',
            field=models.FileField(blank=True, default=None, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]