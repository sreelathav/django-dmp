# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-16 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmp', '0011_auto_20161212_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='DOGstats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('stat_type', models.CharField(max_length=200)),
                ('active_grants', models.IntegerField(null=True)),
                ('contacted_grants', models.IntegerField(null=True)),
                ('dmps_accepted', models.IntegerField(null=True)),
                ('no_data', models.IntegerField(null=True)),
                ('complete_grants', models.IntegerField(null=True)),
                ('ended_with_outstanding_data', models.IntegerField(null=True)),
                ('total_grants', models.IntegerField(null=True)),
            ],
        ),
    ]
