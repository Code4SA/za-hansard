# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionPaper'
        db.create_table('za_hansard_questionpaper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_name', self.gf('django.db.models.fields.TextField')(max_length=32)),
            ('date_published', self.gf('django.db.models.fields.DateField')()),
            ('house', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('document_number', self.gf('django.db.models.fields.IntegerField')()),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=1000)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('issue_number', self.gf('django.db.models.fields.IntegerField')()),
            ('parliament_number', self.gf('django.db.models.fields.IntegerField')()),
            ('session_number', self.gf('django.db.models.fields.IntegerField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('za_hansard', ['QuestionPaper'])

        # Adding unique constraint on 'QuestionPaper', fields ['year', 'issue_number']
        db.create_unique('za_hansard_questionpaper', ['year', 'issue_number'])

        # Adding field 'Question.paper'
        db.add_column('za_hansard_question', 'paper',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['za_hansard.QuestionPaper'], null=True, on_delete=models.SET_NULL),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'QuestionPaper', fields ['year', 'issue_number']
        db.delete_unique('za_hansard_questionpaper', ['year', 'issue_number'])

        # Deleting model 'QuestionPaper'
        db.delete_table('za_hansard_questionpaper')

        # Deleting field 'Question.paper'
        db.delete_column('za_hansard_question', 'paper_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'instances.instance': {
            'Meta': {'object_name': 'Instance'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created_instances'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('instances.fields.DNSLabelField', [], {'unique': 'True', 'max_length': '63', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'instances'", 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'speeches.section': {
            'Meta': {'ordering': "('id',)", 'unique_together': "(('parent', 'slug'),)", 'object_name': 'Section'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['speeches.Section']"}),
            'slug': ('sluggable.fields.SluggableField', [], {'unique_with': "('parent',)", 'max_length': '50', 'populate_from': "'title'"}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'speeches.slug': {
            'Meta': {'object_name': 'Slug'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'redirect': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'za_hansard.answer': {
            'Meta': {'object_name': 'Answer'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'house': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'number_oral': ('django.db.models.fields.TextField', [], {}),
            'number_written': ('django.db.models.fields.TextField', [], {}),
            'processed_code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'za_hansard.pmgcommitteeappearance': {
            'Meta': {'object_name': 'PMGCommitteeAppearance'},
            'committee': ('django.db.models.fields.TextField', [], {}),
            'committee_url': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.TextField', [], {}),
            'meeting_date': ('django.db.models.fields.DateField', [], {}),
            'meeting_url': ('django.db.models.fields.TextField', [], {}),
            'party': ('django.db.models.fields.TextField', [], {}),
            'person': ('django.db.models.fields.TextField', [], {}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appearances'", 'null': 'True', 'to': "orm['za_hansard.PMGCommitteeReport']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'za_hansard.pmgcommitteereport': {
            'Meta': {'object_name': 'PMGCommitteeReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sayit_import': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_url': ('django.db.models.fields.TextField', [], {}),
            'premium': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sayit_section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['speeches.Section']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'za_hansard.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question'", 'null': 'True', 'to': "orm['za_hansard.Answer']"}),
            'askedby': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'document': ('django.db.models.fields.TextField', [], {}),
            'house': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {}),
            'last_sayit_import': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'number1': ('django.db.models.fields.TextField', [], {}),
            'number2': ('django.db.models.fields.TextField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['za_hansard.QuestionPaper']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'parliament': ('django.db.models.fields.TextField', [], {}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'questionto': ('django.db.models.fields.TextField', [], {}),
            'sayit_section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['speeches.Section']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'session': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'translated': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.TextField', [], {})
        },
        'za_hansard.questionpaper': {
            'Meta': {'unique_together': "(('year', 'issue_number'),)", 'object_name': 'QuestionPaper'},
            'date_published': ('django.db.models.fields.DateField', [], {}),
            'document_name': ('django.db.models.fields.TextField', [], {'max_length': '32'}),
            'document_number': ('django.db.models.fields.IntegerField', [], {}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_number': ('django.db.models.fields.IntegerField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'parliament_number': ('django.db.models.fields.IntegerField', [], {}),
            'session_number': ('django.db.models.fields.IntegerField', [], {}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'za_hansard.source': {
            'Meta': {'ordering': "['-date', 'document_name']", 'object_name': 'Source'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'document_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'document_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is404': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'last_processing_attempt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_processing_success': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_sayit_import': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sayit_section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['speeches.Section']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['za_hansard']