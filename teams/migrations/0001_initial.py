# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import teams.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kaleo', '__first__'),
        ('reversion', '0001_initial')
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=20, choices=[(b'applied', b'applied'), (b'invited', b'invited'), (b'declined', b'declined'), (b'rejected', b'rejected'), (b'accepted', b'accepted'), (b'auto-joined', b'auto joined')])),
                ('role', models.CharField(default=b'member', max_length=20, choices=[(b'member', b'member'), (b'manager', b'manager'), (b'owner', b'owner')])),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('invite', models.ForeignKey(related_name='memberships', blank=True, to='kaleo.JoinInvitation', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('avatar', models.ImageField(upload_to=teams.models.avatar_upload, blank=True)),
                ('description', models.TextField(blank=True)),
                ('member_access', models.CharField(max_length=20, choices=[(b'open', b'open'), (b'application', b'by application'), (b'invitation', b'by invitation')])),
                ('manager_access', models.CharField(max_length=20, choices=[(b'add someone', b'add someone'), (b'invite someone', b'invite someone')])),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('creator', models.ForeignKey(related_name='teams_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='membership',
            name='team',
            field=models.ForeignKey(related_name='memberships', to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(related_name='memberships', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('team', 'user', 'invite')]),
        ),
    ]
