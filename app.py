from flask import Flask, render_template, request, abort, make_response, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from base.validate_file_format import allowed_file
from ai.matrix_generator import generate_matrix, generate_response, preprocess_docx, build_message, extraction
from flask import redirect, url_for


# Set the upload and download folders.
main_path = os.path.dirname(os.path.abspath(__file__))
upload_folder = main_path + r"\\static\\input\\"
download_folder = main_path + r"\\static\\output\\"
max_file_size = 32 * 1024 * 1024  # 32 MB

# Create the app and first configuration.
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = max_file_size


# Routes.
@app.route('/')
def index():
    """Return index template."""

    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file."""

    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Here you should save the file
            file.save(upload_folder + filename)
            
            cost, msg = generate_matrix(filename, 'online')
        
            return render_template('upload_success.html', cost=cost, msg=msg)

    return 'Fallo en el subida del archivo, puede que el formato no sea el correcto (docx).'


@app.route("/download")
def download_file():
    """Download a file."""

    list_files = os.listdir(download_folder)

    return render_template('list_generated_files.html', files=list_files)


@app.errorhandler(413)
def too_large(e):
    """Return a custom 413 error."""

    message = "El archivo es demasiado grande. Más de " + str(max_file_size) + " MB."
    return make_response(jsonify(message=message), 413)


#  Run the app.
if __name__ == '__main__':
    app.run(debug=True)
