# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import json

# configuration
from secrets import DATABASE, SECRET_KEY, USERNAME, PASSWORD
DEBUG = True

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/view/<searchterm>')
def show_entries(searchterm):
    print 'searchterm = %s' % searchterm
    cur = g.db.execute('select * from tweets '
                       'where searchterm = ? '
                       'order by timestamp desc '
                       'limit 100', (searchterm,))

    entries = [dict(timestamp=row[0], username=row[1], body=row[2],
                    media=row[3], approved=row[4]) 
               for row in cur.fetchall()]
    # print json.dumps(entries, indent=2)
    return render_template('gallery.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
