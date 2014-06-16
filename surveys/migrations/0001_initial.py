# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SurveyQuestion'
        db.create_table(u'surveys_surveyquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('integer_question', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'surveys', ['SurveyQuestion'])

        # Adding model 'SurveyAnswer'
        db.create_table(u'surveys_surveyanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quesiton', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.SurveyQuestion'])),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'surveys', ['SurveyAnswer'])


    def backwards(self, orm):
        # Deleting model 'SurveyQuestion'
        db.delete_table(u'surveys_surveyquestion')

        # Deleting model 'SurveyAnswer'
        db.delete_table(u'surveys_surveyanswer')


    models = {
        u'surveys.surveyanswer': {
            'Meta': {'object_name': 'SurveyAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quesiton': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.SurveyQuestion']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'surveys.surveyquestion': {
            'Meta': {'object_name': 'SurveyQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integer_question': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['surveys']