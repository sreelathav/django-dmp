# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-20 14:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dmp', '0031_grant_programme'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sciSupContact2',
            field=models.ForeignKey(blank=True, help_text=b'CEDA person contact for this Project', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sciSupContact2s', to='dmp.Person'),
        ),
    ]
