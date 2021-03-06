from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    jsonify,
    url_for
    )
from sqlalchemy import (
    create_engine,
    exc
    )
from sqlalchemy.orm import sessionmaker
from init_db import Base, Author, Book, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///authors.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# -----------------------------------------------------------------------------
# --Author Section ------------------------------------------------------------
# -----------------------------------------------------------------------------
# -- CREATE -------------------------------------------------------------------
# Create a new author
@app.route('/author/new/', methods=['GET', 'POST'])
@login_required
def newAuthor():
    if request.method == 'POST':
        newAuthor = Author(name=request.form['name'],
                           user_id=login_session['gplus_id'])
        session.add(newAuthor)
        session.commit()
        return redirect(url_for('showAuthors'))
    else:
        return render_template('newAuthor.html')


# -- READ ---------------------------------------------------------------------
# Show all authors
@app.route('/')
@app.route('/author/')
def showAuthors():
    authors = session.query(Author).all()
    if 'username' not in login_session:
        return render_template('authorsReadOnly.html', authors=authors)
    return render_template('authors.html', authors=authors)


# -- UPDATE -------------------------------------------------------------------
# Edit Author
@app.route('/author/<int:author_id>/edit/', methods=['GET', 'POST'])
@login_required
def editAuthor(author_id):
    editedAuthor = session.query(
        Author).filter_by(id=author_id).one()
    if editedAuthor.user_id != login_session['email']:
        flash("""You are not authorized to edit this author. Please create
              a new author.""")
        return redirect(url_for('newAuthor'))
    if request.method == 'POST':
        if request.form['name']:
            editedAuthor.name = request.form['name']
            session.add(editedAuthor)
            session.commit()
            return redirect(url_for('showAuthors'))
    else:
        return render_template(
            'editAuthor.html', author=editedAuthor)


# -- DESTROY ------------------------------------------------------------------
# Delete Author
@app.route('/author/<int:author_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteAuthor(author_id):
    authorToDelete = session.query(
        Author).filter_by(id=author_id).one()
    if authorToDelete.user_id != login_session['email']:
        return """<script>function myFunction() {alert('You are not authorized
               to delete this author.');
               window.location.href='http://localhost:5000/author/';}</script>
               <body onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(authorToDelete)
        session.commit()
        return redirect(
            url_for('showAuthors', author_id=author_id))
    else:
        return render_template(
            'deleteAuthor.html', author=authorToDelete)


# -- JSON --------------------------------------------------------
@app.route('/author/JSON')
def authorsJSON():
    authors = session.query(Author).all()
    return jsonify(authors=[a.serialize for a in authors])


# -----------------------------------------------------------------------------
# --Books Section -------------------------------------------------------------
# -----------------------------------------------------------------------------

# -- CREATE -------------------------------------------------------------------

# Create a new book
@app.route(
    '/author/<int:author_id>/book/new/', methods=['GET', 'POST'])
@login_required
def newBook(author_id):
    if request.method == 'POST':
        newBook = Book(title=request.form['title'], description=request.form[
                       'description'], author_id=author_id,
                       user_id=login_session['gplus_id'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('showBookList', author_id=author_id))
    else:
        return render_template('newBook.html', author_id=author_id)


# -- READ ---------------------------------------------------------------------

# Show authors booklist
@app.route('/author/<int:author_id>/')
@app.route('/author/<int:author_id>/booklist/')
def showBookList(author_id):
    author = session.query(Author).filter_by(id=author_id).one()
    books = session.query(Book).filter_by(
        author_id=author_id).all()
    if 'username' not in login_session:
        return render_template('booklistReadOnly.html', books=books,
                               author=author)
    return render_template('booklist.html', books=books, author=author)


# -- UPDATE -------------------------------------------------------------------

# Edit book
@app.route('/author/<int:author_id>/book/<int:book_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editBook(author_id, book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    if editedBook.user_id != login_session['email']:
        return """<script>function myFunction() {alert('You are not authorized
               to edit books for this author. Please create a new author to
               add/edit items.');
               window.location.href='http://localhost:5000/author/';}</script>
               <body onload='myFunction()'>"""
    if request.method == 'POST':
        if request.form['title']:
            editedBook.title = request.form['title']
        if request.form['description']:
            editedBook.description = request.form['description']
        session.add(editedBook)
        session.commit()
        return redirect(url_for('showBookList', author_id=author_id))
    else:

        return render_template(
            'editBook.html', author_id=author_id, book_id=book_id,
            item=editedBook)


# -- DESTROY ------------------------------------------------------

# Delete book
@app.route('/author/<int:author_id>/book/<int:book_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteBook(author_id, book_id):
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    if bookToDelete.user_id != login_session['email']:
        return """<script>function myFunction() {alert('You are not authorized
               to delete books for this author. Please create your own author
               in order to delete books.');}</script><body
               onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        return redirect(url_for('showBookList', author_id=author_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)


# -- JSON ---------------------------------------------------------
@app.route('/author/<int:author_id>/booklist/JSON')
def booklistJSON(author_id):
    author = session.query(Author).filter_by(id=author_id).one()
    books = session.query(Book).filter_by(
        author_id=author_id).all()
    return jsonify(Books=[b.serialize for b in books])


@app.route('/author/<int:author_id>/booklist/<int:book_id>/JSON')
def bookJSON(author_id, book_id):
    Book_Info = session.query(Book).filter_by(id=book_id).one()
    return jsonify(Book_Info=Book_Info.serialize)


# -----------------------------------------------------------------------------
# --Authentication Section ----------------------------------------------------
# -----------------------------------------------------------------------------
@app.route('/gdisconnect', methods=['POST', 'GET'])
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
                    'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                        'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['id']

    # test if user is in db if not create one
    user_id = getUserID(data["id"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
#    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(id=login_session['email']).first()
    return user


def getUserInfo(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except exc.SQLAlchemyError as e:
        print "Unable to getUserInfo: ", str(e)
        return None


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except exc.SQLAlchemyError as e:
        print "Unable to getUserID: ", str(e)
        return None


# -- MAIN --------------------------------------------------------------------
if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
