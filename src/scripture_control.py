import flask  # @UnresolvedImport
import auth
import model
from main import app
import util
from flask import jsonify, request, Response  # @UnresolvedImport
import json  # @UnresolvedImport

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/scriptures/')
@auth.login_required
def scriptures():
#   volume_dbs, more_cursor = util.retrieve_dbs(model.Volume.query(), order='volume_id')
  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scriptures',
                               title='Scripture Selector',
                               volume_name= 'None',
                               book_name= 'None',
                               chapter_num= 'None')
  
@app.route('/scriptures/<volume_name>/')
@auth.login_required
def scriptures_volume(volume_name):
  print volume_name;
#   volume_dbs, more_cursor = util.retrieve_dbs(model.Volume.query(), order='volume_id')
  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scripture',
                               title='Scripture Selector',
                               volume_name=volume_name,
                               book_name= 'None',
                               chapter_num= 'None')

@app.route('/scriptures/<volume_name>/<book_name>/')
@auth.login_required
def scriptures_book(volume_name, book_name):
  print volume_name, book_name;
#   volume_dbs, more_cursor = util.retrieve_dbs(model.Volume.query(), order='volume_id')
  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scripture',
                               title='Scripture Selector',
                               volume_name=volume_name,
                               book_name=book_name,
                               chapter_num= 'None')

@app.route('/scriptures/<volume_name>/<book_name>/<int:chapter_num>')
@auth.login_required
def scriptures_chapter(volume_name, book_name, chapter_num):
  print volume_name, book_name, chapter_num;
#   volume_dbs, more_cursor = util.retrieve_dbs(model.Volume.query(), order='volume_id')
  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scripture',
                               title='Scripture Selector',
                               volume_name=volume_name,
                               book_name=book_name,
                               chapter_num=chapter_num)
  
@app.route('/get_verses/')
@auth.login_required
def get_verses():
  print "get verses baby"
  book = request.args.get('book', 0, type=int)
  chapter_id = request.args.get('chapter_id', 0, type=int)
  print "book ", book
  print "chapter_id ", chapter_id
  query = model.Verse.query(model.Verse.book_id == book, # @UndefinedVariable
                            model.Verse.chapter == chapter_id).order(model.Verse.verse_id);
  verse_dbs = query.fetch();
  myArray = []
  for v in verse_dbs:
    myArray.append(v.to_readable_dict())
  j = json.dumps(myArray)
  return j
  
@app.route('/volume/')
@auth.login_required
def volume_list():
  volume_dbs, more_cursor = util.retrieve_dbs(
                                               model.Volume.query()# @UndefinedVariable
                                               )
  return flask.render_template(
                               'volume_list.html',
                               html_class='volume-list',
                               title='Volume List',
                               volume_dbs=volume_dbs,
                               more_url=util.generate_more_url(more_cursor),
                               )

@app.route('/verse/')
@auth.login_required
def verse_list():
  verse_dbs, more_cursor = util.retrieve_dbs(
                                               model.Verse.query(),# @UndefinedVariable
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
