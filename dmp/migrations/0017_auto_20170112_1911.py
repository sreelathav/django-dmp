# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-12 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmp', '0016_auto_20161223_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ODMP_URL',
            field=models.URLField(blank=True, help_text=b'Outline DMP URL autogenerated when using grant uploader, essentially a best guess. Edit as necessary.', null=True),
        ),
    ]
