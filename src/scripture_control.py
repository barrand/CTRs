from flaskext import wtf 
import flask  # @UnresolvedImport
import auth
import model
from main import app
import util
from flask import jsonify, request, Response  # @UnresolvedImport
import json  # @UnresolvedImport
from scripture_objects import volumesObjects;

@app.route('/scriptures/')
@auth.login_required
def scriptures():
#   volume_dbs, more_cursor = util.retrieve_dbs(model.Volume.query(), order='volume_id')
  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scriptures',
                               title='Scripture Selector',
                               volumesObjects=volumesObjects)
  
@app.route('/scriptures/<volume_name>/')
@auth.login_required
def scriptures_volume(volume_name):
#   volume_dbs, more_cursor = util.retrieve_dbs(model.Volume.query(), order='volume_id')
  selectedVolume = volumesObjects[volume_name]
  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scripture',
                               title='Scripture Selector',
                               selectedVolume=selectedVolume,
                               volumeName=volume_name)

@app.route('/scriptures/<volume_name>/<book_name>/')
@auth.login_required
def scriptures_book(volume_name, book_name):
  print volume_name, book_name;
  selectedVolume = volumesObjects[volume_name]
  selectedBook = selectedVolume["books"][book_name]
  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scripture',
                               title='Scripture Selector',
                               selectedVolume=selectedVolume,
                               selectedBook=selectedBook,
                               volumeName=volume_name,
                               bookName=book_name)

@app.route('/scriptures/<volume_name>/<book_name>/<int:chapter_num>')
@auth.login_required
def scriptures_chapter(volume_name, book_name, chapter_num):
  selectedVolume = volumesObjects[volume_name]
  selectedBook = selectedVolume["books"][book_name]
  query = model.Verse.query(model.Verse.book_id == selectedBook['book_id'],
                            model.Verse.chapter == chapter_num).order(model.Verse.verse_id)
  verse_dbs = query.fetch()

  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scripture',
                               title='Scripture Selector',
                               selectedVolume=selectedVolume,
                               selectedBook=selectedBook,
                               chapterNum=chapter_num,
                               volumeName=volume_name,
                               bookName=book_name,
                               verse_dbs=verse_dbs)

@app.route('/scriptures/<volume_name>/<book_name>/<int:chapter_num>/<int:verse_num>', methods=['GET', 'POST'])
@auth.login_required
def scriptures_verse(volume_name, book_name, chapter_num, verse_num):
  selectedVolume = volumesObjects[volume_name]
  selectedBook = selectedVolume["books"][book_name]
  
  query = model.Verse.query(model.Verse.book_id == selectedBook['book_id'],
                            model.Verse.chapter == chapter_num).order(model.Verse.verse_id)
  verse_dbs = query.fetch()

  verse_id = None
  for tmpverse in verse_dbs:
    if tmpverse.verse == verse_num:
      verse_id = tmpverse.verse_id
  
  form = CommentAddForm()
  if form.validate_on_submit():
    comment_db = model.Comment(
        user_key=auth.current_user_key(),
        comment=form.comment.data,
        verse_id=verse_id,
        commentType=form.commentType.data,
      )
    comment_db.put()
    flask.flash('New comment was successfuly created!', category='success')

  query = model.Comment.query(model.Comment.verse_id == verse_id).order(-model.Verse.created)
  comment_dbs = query.fetch()
  for c in comment_dbs:
    c.userObject = c.user_key.get()

  return flask.render_template(
                               'scripture_selector.html',
                               html_class='scripture',
                               title='Scripture Selector',
                               selectedVolume=selectedVolume,
                               selectedBook=selectedBook,
                               chapterNum=chapter_num,
                               volumeName=volume_name,
                               bookName=book_name,
                               verse_dbs=verse_dbs,
                               verseNum=verse_num,
                               form=form,
                               comment_dbs=comment_dbs
                               )
  

class CommentAddForm(wtf.Form):
  comment = wtf.TextAreaField('Comment', [wtf.validators.required()])
  commentType = wtf.RadioField('CommentType', choices=[('comment', 'comment'), 
        ('question', 'question'), 
        ('crossreference', 'cross reference')],
        default='comment')



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

@app.template_filter()
def get_username_by_user_key(user_key):
    user = user_key.get()
    return user.username

@app.template_filter()
def get_usericon_by_user_key(user_key):
    user = user_key.get()
    return user.avatar_url

@app.template_filter()
def get_pretty_date(date):
    return date.strftime("%b %d %Y")

@app.template_filter()
def comment_is_question(commentType):
    return commentType == 'question'
