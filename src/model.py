# -*- coding: utf-8 -*-

from google.appengine.ext import ndb  # @UnresolvedImport
from uuid import uuid4  # @UnresolvedImport
import os
import modelx


# The timestamp of the currently deployed version
TIMESTAMP = long(os.environ.get('CURRENT_VERSION_ID').split('.')[1]) >> 28


class Base(ndb.Model, modelx.BaseX):
  created = ndb.DateTimeProperty(auto_now_add=True)
  modified = ndb.DateTimeProperty(auto_now=True)
  version = ndb.IntegerProperty(default=TIMESTAMP)
  _PROPERTIES = set([
      'key',
      'id',
      'version',
      'created',
      'modified',
    ])
  


class Config(Base, modelx.ConfigX):
  analytics_id = ndb.StringProperty(default='')
  announcement_html = ndb.StringProperty(default='')
  announcement_type = ndb.StringProperty(default='info', choices=[
      'info', 'warning', 'success', 'danger',
    ])
  brand_name = ndb.StringProperty(default='CTRs')
  facebook_app_id = ndb.StringProperty(default='')
  facebook_app_secret = ndb.StringProperty(default='')
  feedback_email = ndb.StringProperty(default='')
  flask_secret_key = ndb.StringProperty(default=str(uuid4()).replace('-', ''))
  twitter_consumer_key = ndb.StringProperty(default='')
  twitter_consumer_secret = ndb.StringProperty(default='')

  _PROPERTIES = Base._PROPERTIES.union(set([
      'analytics_id',
      'announcement_html',
      'announcement_type',
      'brand_name',
      'facebook_app_id',
      'facebook_app_secret',
      'feedback_email',
      'flask_secret_key',
      'twitter_consumer_key',
      'twitter_consumer_secret',
    ]))


class User(Base, modelx.UserX):
  name = ndb.StringProperty(indexed=True, required=True)
  username = ndb.StringProperty(indexed=True, required=True)
  email = ndb.StringProperty(indexed=True, default='')

  active = ndb.BooleanProperty(default=True)
  admin = ndb.BooleanProperty(default=False)

  federated_id = ndb.StringProperty(indexed=True, default='')
  facebook_id = ndb.StringProperty(indexed=True, default='')
  twitter_id = ndb.StringProperty(indexed=True, default='')

  _PROPERTIES = Base._PROPERTIES.union(set([
      'name',
      'username',
      'avatar_url',
    ]))


class Contact(Base):
  user_key = ndb.KeyProperty(kind=User, required=True)
  name = ndb.StringProperty(required=True)
  email = ndb.StringProperty(default='')
  phone = ndb.StringProperty(default='')
  address = ndb.StringProperty(default='')
  

class Verse(Base):
  verse_id = ndb.IntegerProperty(required=True)
  volume_id = ndb.IntegerProperty(required=True)
  book_id = ndb.IntegerProperty(required=True)
  chapter = ndb.IntegerProperty(required=True)
  verse = ndb.IntegerProperty(required=True)
  verse_scripture = ndb.TextProperty(required=True)
  
  def to_readable_dict(self):
    d = {}
    d['verse_id']= self.verse_id 
    d['volume_id']= self.volume_id 
    d['chapter']= self.chapter 
    d['verse']= self.verse 
    d['verse_scripture']= self.verse_scripture 
    return d

class Comment(Base):
  user_key = ndb.KeyProperty(kind=User, required=True)
  comment = ndb.TextProperty(required=True)
  like_count = ndb.IntegerProperty(required=False, default=0)
  verse_id = ndb.IntegerProperty(required=True)
  commentType = ndb.StringProperty(required=True)
  tags = ndb.StringProperty(repeated=True)
  inReplyToCommentId = ndb.IntegerProperty(required=False)
  active = ndb.BooleanProperty(default=True)
# references

  