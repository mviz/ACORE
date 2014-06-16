# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SurveyQuestion.question_index'
        db.add_column(u'surveys_surveyquestion', 'question_index',
                      self.gf('django.db.models.fields.IntegerField')(default=-1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SurveyQuestion.question_index'
        db.delete_column(u'surveys_surveyquestion', 'question_index')


    models = {
        u'surveys.surveyanswer': {
            'Meta': {'object_name': 'SurveyAnswer'},
            'answer_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quesiton': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.SurveyQuestion']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'surveys.surveyquestion': {
            'Meta': {'ordering': "['question_index']", 'object_name': 'SurveyQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integer_question': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'question_index': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        }
    }

    complete_apps = ['surveys']