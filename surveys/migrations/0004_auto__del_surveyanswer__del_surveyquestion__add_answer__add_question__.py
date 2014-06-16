# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SurveyAnswer'
        db.delete_table(u'surveys_surveyanswer')

        # Deleting model 'SurveyQuestion'
        db.delete_table(u'surveys_surveyquestion')

        # Adding model 'Answer'
        db.create_table(u'surveys_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quesiton', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Question'])),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('answer_text', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
        ))
        db.send_create_signal(u'surveys', ['Answer'])

        # Adding model 'Question'
        db.create_table(u'surveys_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('integer_question', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('question_index', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal(u'surveys', ['Question'])

        # Adding unique constraint on 'Question', fields ['question', 'question_index']
        db.create_unique(u'surveys_question', ['question', 'question_index'])


    def backwards(self, orm):
        # Removing unique constraint on 'Question', fields ['question', 'question_index']
        db.delete_unique(u'surveys_question', ['question', 'question_index'])

        # Adding model 'SurveyAnswer'
        db.create_table(u'surveys_surveyanswer', (
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('answer_text', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quesiton', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.SurveyQuestion'])),
        ))
        db.send_create_signal(u'surveys', ['SurveyAnswer'])

        # Adding model 'SurveyQuestion'
        db.create_table(u'surveys_surveyquestion', (
            ('question_index', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('integer_question', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=256)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'surveys', ['SurveyQuestion'])

        # Deleting model 'Answer'
        db.delete_table(u'surveys_answer')

        # Deleting model 'Question'
        db.delete_table(u'surveys_question')


    models = {
        u'surveys.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quesiton': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Question']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'surveys.question': {
            'Meta': {'ordering': "['question_index']", 'unique_together': "[['question', 'question_index']]", 'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integer_question': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'question_index': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        }
    }

    complete_apps = ['surveys']