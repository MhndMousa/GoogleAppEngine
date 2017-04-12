from flask import Flask, render_template, request

from google.appengine.api import memcache, users, images, urlfetch
from google.appengine.ext import ndb

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.



@app.route('/')
def counter():

    url = 'http://www.google.com/humans.txt'
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            uindy = result.content
        else:
            response.status_code = result.status_code
    except urlfetch.Error:
        logging.exception('Caught exception fetching url')


    user = users.get_current_user()
    if user:
      #return str(dir(user))
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
      if request.method == 'GET' and 'favorite_class' in request.args:
        major = request.args['favorite_class']
        # Check to see if that name is in names
        names = memcache.get('names')
        if major in names.split('/'):
        	# that person is already there
        	memcache.incr(major)
        else:
          memcache.set('names', names + '/' + major)
          memcache.set(major,1)
      names = memcache.get('names').split('/')
      counts = []
      for n in names:
        counts.append( (n, memcache.get(n)))

      return render_template('counter.html', counts=counts, face= major, nick = user.nickname(), uindy = uindy )


    else:
      login_url = users.create_login_url('/')
      return 'Sorry, you are not logged in. <a href="%s">login</a>' % login_url, 200








@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
