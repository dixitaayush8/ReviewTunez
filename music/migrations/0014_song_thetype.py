# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-02 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_auto_20180102_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='theType',
            field=models.CharField(default='No type', max_length=10),
        ),
    ]
