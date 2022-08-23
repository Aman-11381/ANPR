import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import scripts.predict as predict

UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)   
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({
                'message': 'No file part in the request.'
            }), 400

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return jsonify({
                'message': 'No file selected.'
            }), 400

        if file and allowed_file(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            plate_number = predict.read_image_file('static/files/' + file.filename)
            return jsonify({
                'message': 'File uploaded successfully.',
                'plate_number': plate_number[:-1],
            }), 200

# function that checks if an extension is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS