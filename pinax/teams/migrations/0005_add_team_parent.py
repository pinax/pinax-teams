# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_teams', '0004_auto_20170511_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleteam',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pinax_teams.SimpleTeam'),
        ),
        migrations.AddField(
            model_name='team',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pinax_teams.Team'),
        ),
    ]
