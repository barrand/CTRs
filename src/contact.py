from flaskext import wtf  # @UnresolvedImport
 
class ContactUpdateForm(wtf.Form):
  name = wtf.TextField('Name', [wtf.validators.required()])
  email = wtf.TextField('Email', [
      wtf.validators.optional(),
      wtf.validators.email('That does not look like an email'),
    ])
  phone = wtf.TextField('Phone', [wtf.validators.optional()])
  address = wtf.TextAreaField('Address', [wtf.validators.optional()])
  
  
import flask  # @UnresolvedImport
import auth
import model
from main import app
 
@app.route('/contact/create/', methods=['GET', 'POST'])
@auth.login_required
def contact_create():
  form = ContactUpdateForm()
  if form.validate_on_submit():
    contact_db = model.Contact(
        user_key=auth.current_user_key(),
        name=form.name.data,
        email=form.email.data,
        phone=form.phone.data,
        address=form.address.data,
      )
    contact_db.put()
    flask.flash('New Contact was successfully created!', category='success')
    return flask.redirect(flask.url_for('contact_list', order='-created'))
  return flask.render_template(
      'contact_create.html',
      html_class='contact-create',
      title='Create Contact',
      form=form,
    )
  
  
import util

@app.route('/contact/')
@auth.login_required
def contact_list():
  contact_dbs, more_cursor = util.retrieve_dbs(
                                               model.Contact.query(), 
                                               limit=util.param('limit', int), 
                                               cursor=util.param('cursor'), 
                                               order=util.param('order'),
                                               )
  return flask.render_template(
                               'contact_list.html',
                               html_class='contact-list',
                               title='Contact List',
                               contact_dbs=contact_dbs,
                               more_url=util.generate_more_url(more_cursor),
                               )