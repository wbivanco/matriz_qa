from flask import Flask, render_template, request, abort, make_response, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from base.validate_file_format import allowed_file


main_path = os.path.dirname(os.path.abspath(__file__))
upload_folder = main_path + r"\\backend\\input\\"




app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 16 MB
app.config['UPLOAD_FOLDER'] = upload_folder



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
            # file.save(app.config['UPLOAD_FOLDER'] + filename)
        

            return 'Archivo subido exitosamente'

    return 'Fallo en el subida del archivo'


@app.route("/download")
def download_file():
    """Download a file."""

    return send_file(main_path + r"\\backend\\output\\documento.docx", as_attachment=True)


@app.errorhandler(413)
def too_large(e):
    """Return a custom 413 error."""

    return make_response(jsonify(message="El archivo es demasiado grande."), 413)


#  Run the app.
if __name__ == '__main__':
    app.run(debug=True)