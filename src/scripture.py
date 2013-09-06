import flask # @UnresolvedImport
import auth
import model
from main import app
import util

VOLUME = 0
BOOK = 1
VERSE = 2
selectedNavLevel = VOLUME

@app.route('/scripture/')
@auth.login_required
def scripture():
  volume_dbs, more_cursor = util.retrieve_dbs(model.Volume.query(), order='volume_id')
  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scripture-selector',
                               title='Scripture Selector',
                               volume_dbs=volume_dbs,
                               more_url=util.generate_more_url(more_cursor),
                               )
  
@app.route('/volume/')
@auth.login_required
def volume_list():
  volume_dbs, more_cursor = util.retrieve_dbs(
                                               model.Volume.query()
                                               )
  return flask.render_template(
                               'volume_list.html',
                               html_class='volume-list',
                               title='Volume List',
                               volume_dbs=volume_dbs,
                               more_url=util.generate_more_url(more_cursor),
                               )

@app.route('/book/')
@auth.login_required
def book_list():
  book_dbs, more_cursor = util.retrieve_dbs(
                                               model.Book.query(), 
                                               limit=util.param('limit', int), 
                                               cursor=util.param('cursor'), 
                                               order=util.param('order'),
                                               )
  return flask.render_template(
                               'book_list.html',
                               html_class='book-list',
                               title='Book List',
                               book_dbs=book_dbs,
                               more_url=util.generate_more_url(more_cursor),
                               )
@app.route('/verse/')
@auth.login_required
def verse_list():
  verse_dbs, more_cursor = util.retrieve_dbs(
                                               model.Verse.query(), 
                                               limit=util.param('limit', 600), 
                                               cursor=util.param('cursor'), 
                                               order=util.param('order'),
                                               )
  return flask.render_template(
                               'verse_list.html',
                               html_class='verse-list',
                               title='Verse List',
                               verse_dbs=verse_dbs,
                               more_url=util.generate_more_url(more_cursor),
                               )
