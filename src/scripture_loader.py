from google.appengine.ext import db
from google.appengine.tools import bulkloader
from google.appengine.ext import ndb
from model import Base

class VolumeLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Volume',
                                   [('volume_id', int),
                                    ('volume_title', str),
                                    ('volume_title_long', str),
                                    ('volume_subtitle', str),
                                    ('lds_org', str),
                                    ('num_books', int),
                                    ('num_chapters', int),
                                    ('num_verses', int)
                                   ])

loaders = [VolumeLoader]



import json  # @UnresolvedImport
import urllib2  # @UnresolvedImport
import auth
import model
import util
from main import app

@app.route('/volume_loader', methods=['GET'])
@auth.login_required
def volume():
    url = 'https://dl.dropboxusercontent.com/u/70607137/9%3A13/lds_scriptures_volumes.json'
    site = urllib2.urlopen(url)
    volumes = json.load(site)
    for v in volumes:
      volume_db = model.Volume(
                               volume_id=v['volume_id'],
                               volume_title=v['volume_title'],
                               volume_title_long=v['volume_title_long'],
                               volume_subtitle=v['volume_subtitle'],
                               lds_org=v['lds_org'],
                               num_books=v['num_books'],
                               num_chapters=v['num_chapters'],
                               num_verses=v['num_verses'],
                               )
      volume_db.put();
      
    string = ""
    volume_dbs = util.retrieve_dbs(model.Volume.query())
    print '--, ', len(volume_dbs);
    return string

@app.route('/book_loader', methods=['GET'])
@auth.login_required
def book():
    url = 'https://dl.dropboxusercontent.com/u/70607137/9%3A13/lds_scriptues_books.json'
    site = urllib2.urlopen(url)
    books = json.load(site)
    for v in books:
      book_db = model.Book(
                               book_id=v['book_id'],
                               volume_id=v['volume_id'],
                               book_title=v['book_title'],
                               book_title_long=v['book_title_long'],
                               book_title_short=v['book_title_short'],
                               book_title_jst=v['book_title_jst'],
                               book_subtitle=v['book_subtitle'],
                               lds_org=v['lds_org'],
                               num_chapters=v['num_chapters'],
                               num_verses=v['num_verses'],
                               )
      book_db.put();
      
    string = ""
    book_dbs = util.retrieve_dbs(model.Book.query())
    print '--, ', len(book_dbs);
    return string

@app.route('/verse_loader', methods=['GET'])
@auth.login_required
def verse():
    url = 'https://dl.dropboxusercontent.com/u/70607137/9%3A13/lds_scriptures_verses.json'
    site = urllib2.urlopen(url)
    verses = json.load(site)
    for v in verses:
      verse_db = model.Verse(
                               verse_id=v['verse_id'],
                               volume_id=v['volume_id'],
                               book_id=v['book_id'],
                               chapter=v['chapter'],
                               verse=v['verse'],
                               verse_scripture=v['verse_scripture'],
                               )
      verse_db.put();
      
    string = ""
    verse_dbs = util.retrieve_dbs(model.Verse.query())
    print '--, ', len(verse_dbs);
    return string
  