# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-26 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_forumtopic_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductStats',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pid', models.IntegerField(default=0)),
                ('uid', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=0)),
                ('like', models.IntegerField(default=0)),
                ('listen', models.IntegerField(default=0)),
                ('download', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='profilepics',
            field=models.TextField(default=''),
        ),
    ]
