# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmp', '0017_draftdmp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='draftdmp',
            options={'verbose_name_plural': 'Draft DMP'},
        ),
        migrations.RenameField(
            model_name='draftdmp',
            old_name='draft_dmp',
            new_name='draft_dmp_content',
        ),
        migrations.AddField(
            model_name='draftdmp',
            name='draft_dmp_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
