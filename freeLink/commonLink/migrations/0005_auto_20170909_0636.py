# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonLink', '0004_auto_20170909_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordcontent',
            name='created_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='keywordcontent',
            name='updated_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='keywordcontent',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]