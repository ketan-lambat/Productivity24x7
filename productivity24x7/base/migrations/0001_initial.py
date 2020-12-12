# Generated by Django 3.1.3 on 2020-12-12 17:05

import colorfield.fields
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
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('duration', models.PositiveIntegerField(default=None, help_text='in minutes', null=True)),
                ('deadline', models.DateTimeField(default=None, null=True)),
                ('is_completed', models.BooleanField(default=None, null=True)),
                ('g_event_id', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=25)),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', max_length=18)),
                ('owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('owner', 'name')},
            },
        ),
        migrations.CreateModel(
            name='EventTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_tags', to='base.event')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='base.tag')),
            ],
        ),
    ]
