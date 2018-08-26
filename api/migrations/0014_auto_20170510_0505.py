# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-10 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20170510_0448'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentText',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fulltext', models.TextField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='textid',
            field=models.IntegerField(default=0),
        ),
    ]
