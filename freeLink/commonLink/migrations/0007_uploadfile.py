# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-11 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonLink', '0006_auto_20170909_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='upload/%Y/%m/%d')),
            ],
        ),
    ]
