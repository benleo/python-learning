# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='post_time',
            field=models.DateTimeField(null=True),
        ),
    ]
