from flask import Flask, render_template, request

from google.appengine.api import memcache, users, images, urlfetch
from google.appengine.ext import ndb

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.



@app.route('/')
def survey():

    url = 'http://www.google.com/humans.txt'
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            google_text = result.content
        else:
            response.status_code = result.status_code
    except urlfetch.Error:
        logging.exception('Caught exception fetching url')




    user = users.get_current_user()
    if user:
      curr_users = memcache.get('curr_users')
      if curr_users:
        if user.nickname() not in curr_users:
          curr_users.append(user.nickname())
          memcache.set('curr_users',curr_users)
      else:
        memcache.set('curr_users',[user.nickname()])
      logout_url = users.create_logout_url('/')
      curr_users = memcache.get('curr_users')




      if 'reset' in request.args:
        memcache.flush_all()
      # set up names if it doesn't exist
      memcache.add('names','')
      major = "Finance"
      if request.method == 'GET' and 'added_major' in request.args:
        major = request.args['added_major']
        # Check to see if that name is in names
        names = memcache.get('names')
        if major in names.split('/'):
        	# that person is already there
        	memcache.incr(major)
        else:
          memcache.set('names', names + '/' + major)
          memcache.set(major,1)
      names = memcache.get('names').split('/')
      majors = []
      for n in names:
        majors.append( (n, memcache.get(n)))




      return render_template('survey.html', majors=majors, add_major= major,
      nick = user.nickname(), google_demo_text = google_text,
      logout_url = logout_url)




    else:
      login_url = users.create_login_url('/')
      return 'You are not logged in. <br> <a href="%s">login</a>' % login_url, 200








@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
