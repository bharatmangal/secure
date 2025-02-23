from flask import Flask, render_template, session, redirect, url_for, send_from_directory, request, make_response
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secure-key'  # Replace with a strong, random key in production

def require_session_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for valid session flag.
        if not session.get('access_granted'):
            return redirect(url_for('index'))
        # Extra measure: verify that the request originates from your site.
        referrer = request.headers.get('Referer', '')
        if not referrer or not referrer.startswith(request.host_url):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acess')
@require_session_access
def access():
    # Only allow access if the session flag is set.
    if not session.get('access_granted'):
        return redirect(url_for('index'))
    return render_template('acess.html')

@app.route('/acessDenies')
def access_denied():
    return render_template('acessDenies.html')

@app.route('/redirect_route')
def redirect_route():
    # Set the session flag for authorized access.
    session['access_granted'] = True
    return redirect(url_for('access'))

# Protected asset routes – these endpoints require a valid session and referer.
@app.route("/webgl/build/data")
@require_session_access
def serve_build_data():
    return send_from_directory("Build", "Export.data")

@app.route("/webgl/build/framework")
@require_session_access
def serve_build_framework():
    return send_from_directory("Build", "Export.framework.js")

@app.route("/webgl/build/loader")
@require_session_access
def serve_build_loader():
    return send_from_directory("Build", "Export.loader.js")

@app.route("/webgl/build/wasm")
@require_session_access
def serve_build_wasm():
    return send_from_directory("Build", "Export.wasm")

@app.route("/loaderio-3669706db4ff2455a390082f75995425/")
def loaderio():
    return render_template("loaderio-3669706db4ff2455a390082f75995425")

@app.route("/get_rooms/<path:filename>")
@require_session_access
def get_streaming_assets(filename):
    return send_from_directory("StreamingAssets", filename)

# Global error handler for any unexpected 403 responses.
@app.errorhandler(403)
def forbidden(e):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)