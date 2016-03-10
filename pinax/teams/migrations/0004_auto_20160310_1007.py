# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_teams', '0003_auto_20160309_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplemembership',
            name='invite',
            field=models.ForeignKey(related_name='simple_memberships', verbose_name='invite', blank=True, to='invitations.JoinInvitation', null=True),
        ),
        migrations.AlterField(
            model_name='simplemembership',
            name='user',
            field=models.ForeignKey(related_name='simple_memberships', verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
