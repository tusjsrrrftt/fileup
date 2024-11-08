import os
import logging
from flask import Flask, render_template, request, redirect, url_for, abort, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        app.logger.info(f"File saved: {file_path}")
    return redirect(url_for('index'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.logger.info(f"Attempting to serve file: {file_path}")

        if not os.path.exists(file_path):
            app.logger.error(f"File not found: {file_path}")
            abort(404, description="File not found")

        def generate():
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    yield chunk

        response = Response(generate(), mimetype='application/octet-stream')
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        return response
    except Exception as e:
        app.logger.error(f"Error serving file {filename}: {str(e)}")
        abort(500, description="Internal server error")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=error), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=error), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)