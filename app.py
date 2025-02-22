from flask import Flask, render_template, session, redirect, url_for, abort
from functools import wraps

app = Flask(__name__)
app.secret_key = '1234'  # Change this to a secure random key

def check_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('access_allowed'):
            # Set a flag so the access_denied page knows it’s an internal redirect
            session['internal_access_denied'] = True
            return redirect(url_for('access_denied'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acess')
@check_access
def access():
    # Only allow access if this route was reached through the proper redirect.
    # If the session flag 'internal_access' is missing, abort with 405.
    if not session.pop('internal_access', False):
        abort(405)
    return render_template('acess.html')

@app.route('/acessDenies')
def access_denied():
    # Only allow internal redirects to this route.
    if not session.pop('internal_access_denied', False):
        abort(405)
    return render_template('acessDenies.html')

@app.route('/redirect_route')
def redirect_route():
    if not session.pop('internal_access_denied', False):
        abort(405)
    # Set the session flags to allow access to the internal pages.
    session['access_allowed'] = True
    session['internal_access'] = True
    return redirect(url_for('access'))

if __name__ == '__main__':
    app.run(debug=True)
