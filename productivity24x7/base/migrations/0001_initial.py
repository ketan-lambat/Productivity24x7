# Generated by Django 3.1.3 on 2020-11-17 21:10

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('key', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('color', colorfield.fields.ColorField(default='#A8A8A8', max_length=18)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('name', models.CharField(max_length=25)),
                ('color', colorfield.fields.ColorField(default='#A8A8A8', max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('duration', models.PositiveIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)])),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('managed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.tag')),
            ],
        ),
    ]
