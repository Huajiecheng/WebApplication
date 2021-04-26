# Generated by Django 3.1.2 on 2020-11-13 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('description', models.CharField(max_length=200)),
                ('entry_type', models.CharField(choices=[('APPETIZER', 'Appetizer'), ('SOUP', 'Soup'), ('SALAD', 'Salad'), ('ENTREE', 'Entree'), ('BEVERAGE', 'Beverage'), ('DESSERT', 'Dessert')], default='', max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction', models.CharField(max_length=200)),
                ('order_time', models.DateTimeField()),
                ('location', models.CharField(default='', max_length=50)),
                ('customer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('items', models.ManyToManyField(to='project.Entry')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
                ('review_photo', models.FileField(blank=True, default=None, upload_to='')),
                ('review_time', models.DateTimeField()),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='project.order')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=200)),
                ('average_rating', models.FloatField()),
                ('photo', models.FileField(blank=True, default=None, upload_to='')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(default='A great restaurant!', max_length=200)),
                ('admin_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.FileField(blank=True, default=None, upload_to='')),
                ('card', models.CharField(default='', max_length=20)),
                ('payment_key', models.CharField(default='', max_length=50)),
                ('location', models.CharField(default='', max_length=50)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='project.Entry')),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='project.profile')),
            ],
        ),
    ]
