# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-21 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmp', '0012_dogstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='grant',
            name='pi_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
