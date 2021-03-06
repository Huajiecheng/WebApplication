# Generated by Django 3.1.3 on 2020-11-26 00:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0008_auto_20201117_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.FloatField()),
                ('state', models.CharField(default='', max_length=20)),
                ('street_1', models.CharField(default='', max_length=200)),
                ('street_2', models.CharField(default='', max_length=200)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
