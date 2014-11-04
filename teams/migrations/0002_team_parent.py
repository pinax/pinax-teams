# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='teams.Team', null=True),
            preserve_default=True,
        ),
    ]
