# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-17 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_device'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='pid',
        ),
        migrations.AddField(
            model_name='transactions',
            name='description',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]