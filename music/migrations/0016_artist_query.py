# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-02 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0015_auto_20180102_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='query',
            field=models.CharField(default='No query', max_length=100),
        ),
    ]