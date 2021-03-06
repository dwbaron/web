# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-01 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=255)),
                ('url', models.URLField()),
                ('text', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
