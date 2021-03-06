# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-03 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmp', '0027_auto_20170615_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='reassigned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[(b'Proposal', b'Proposal'), (b'NotFunded', b'Not Funded'), (b'NotStarted', b'Not Started'), (b'Active', b'Active'), (b'NoData', b'No Data'), (b'EndedWithDataToCome', b'Ended with data to come'), (b'Defaulted', b'Defaulted'), (b'NoDataForUs', b'No data for us'), (b'Complete', b'Complete'), (b'Unresponsive', b'Unresponsive'), (b'MergedProject/HandledElsewhere', b'Merged Project/Handled Elsewhere')], max_length=200, null=True),
        ),
    ]
