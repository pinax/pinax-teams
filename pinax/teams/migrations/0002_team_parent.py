# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='parent',
            field=models.ForeignKey(related_name=b'children', blank=True, to='pinax_teams.Team', null=True),
        ),
    ]
