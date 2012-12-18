from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
import recognizer
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1><a href="{}">click here for feedback</a></h1>'.format(url_for('feedback'))

@app.route('/report', methods=['GET', 'POST'])
def report ():
    code = request.form['code']
    errors = request.form['errors']

    return recognizer.diagnose(code, errors)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Registers the user."""
    return render_template('feedback.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
