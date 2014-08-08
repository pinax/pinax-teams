# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("reversion", "0007_auto__del_field_version_type"),
    )

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table(u'teams_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('member_access', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('manager_access', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teams_created', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'teams', ['Team'])

        # Adding model 'Membership'
        db.create_table(u'teams_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['teams.Team'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', null=True, to=orm['auth.User'])),
            ('invite', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', null=True, to=orm['kaleo.JoinInvitation'])),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('role', self.gf('django.db.models.fields.CharField')(default='member', max_length=20)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'teams', ['Membership'])

        # Adding unique constraint on 'Membership', fields ['team', 'user', 'invite']
        db.create_unique(u'teams_membership', ['team_id', 'user_id', 'invite_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Membership', fields ['team', 'user', 'invite']
        db.delete_unique(u'teams_membership', ['team_id', 'user_id', 'invite_id'])

        # Deleting model 'Team'
        db.delete_table(u'teams_team')

        # Deleting model 'Membership'
        db.delete_table(u'teams_membership')


    models = {
        u'kaleo.joininvitation': {
            'Meta': {'object_name': 'JoinInvitation'},
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invites_sent'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'signup_code': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.SignupCode']", 'unique': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invites_received'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'teams.membership': {
            'Meta': {'unique_together': "[('team', 'user', 'invite')]", 'object_name': 'Membership'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'null': 'True', 'to': u"orm['kaleo.JoinInvitation']"}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'member'", 'max_length': '20'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['teams.Team']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams_created'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_access': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'member_access': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['teams']