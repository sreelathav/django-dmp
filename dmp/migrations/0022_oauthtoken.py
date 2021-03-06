# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-13 15:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dmp', '0021_auto_20170113_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_expiry', models.DateTimeField()),
                ('id_token', models.CharField(max_length=200)),
                ('access_token', models.CharField(max_length=200)),
                ('invalid', models.CharField(max_length=200)),
                ('refresh_token', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='oauth_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OAuth Token',
            },
        ),
    ]
