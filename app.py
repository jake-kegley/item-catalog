import requests
import random
import string
import json
import httplib2

from flask import Flask 
from flask import redirect, render_template, url_for
from flask import session as login_session
from flask import flash, make_response, request
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Item, Category

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = ('ItemCatalog')

engine = create_engine('sqlite://catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
	categories = session.query(Category).all()
	return render_template('home.html', categories=categories)


@app.route('/login')
def login():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	code = request.data

	try:
		oauth_flow = flow_from_clientsecrets('client_secrets', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps("Failed to upgrade the auth code", 401))
		response.headers['Content-Type'] = 'application/json'
		return response

	access_token = credentials.access_token
	url = ('htpps://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()

	result = json.loads(h.request(url, 'GET')[1])

	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token Id does not match users"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps('Token client ID does not match app.'), 401)
		print "Tokens client id does not match"
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials =  login_session.get('credentials')
	stored_gplus_id =  login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		resopnse = make_response(json.dumps('Current user already connected'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id

	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	output = ''
	output = '<h1>Welcome,'
	output = login_session['username']
	output = '!</h1>'
	output = '<img src="'
	output = login_session['picture']
	output = '" style="width: 300px; height: 300px; border-radius: 150px;'
	flash("You are now logged in as %s" % login_session['username'])
	print "DONE!"
	return output

def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session[
					'email'], picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id

def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user

def getUserId(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None
@app.route('/gdisconnect')
def gdisconnect():
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response 
	access_token = credentials.access_token
	url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
	else:
		response = make_response(json.dumps('failed to revoke token for some reason'), 400)
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/dashboard')
def dashboard():
	if 'username' not in login_session:
		return redirect('/login')
	categories = session.query(Category).all()
	return render_template('dashboard', categories = categories)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)


