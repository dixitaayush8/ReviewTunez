# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-02 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0012_auto_20180102_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='markets',
        ),
        migrations.RemoveField(
            model_name='album',
            name='tracks',
        ),
        migrations.RemoveField(
            model_name='song',
            name='markets',
        ),
        migrations.AddField(
            model_name='album',
            name='theType',
            field=models.CharField(default='No type', max_length=10),
        ),
    ]
