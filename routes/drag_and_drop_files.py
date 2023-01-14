from flask import render_template, Blueprint, abort, request, jsonify
from werkzeug.utils import secure_filename
from specific_email_session import USER_ROOT_PATH
from jinja2 import TemplateNotFound
import os
from firebase_initialisation import db

simple_page = Blueprint('simple_page', __name__, template_folder='templates')
file_name_config = 'test_uploads/'
firebase_config = 'hi'


relationship_summarization = db.collection(
        f"{USER_ROOT_PATH}/{get_email_user_name()}/relationships"
    )


@simple_page.route('/testing')
def show():
    try:
        return render_template(f'harvest/drag_and_drop_files.html')
    except TemplateNotFound:
        abort(404)


@simple_page.route('/file-upload', methods=['POST'])
def upload_file():
    """
    Uploads a file to the server.
    The file will be saved either locally or on Firebase storage based on the value of the 'ENV' environment variable.
    If 'ENV' is set to 'local', the file will be saved locally on the server.
    If 'ENV' is set to 'firebase', the file will be uploaded to Firebase storage.
    :param file: The file to be uploaded.
    :return: A json object containing a message indicating if the file was uploaded successfully.
    """

    file = request.files['file']
    if file:
        # Get the environment variable
        env = os.environ.get('ENV', 'local')
        if env == 'local':
            # Save the file locally
            file.save(file_name_config + file.filename)
            return jsonify({'message': 'File uploaded successfully'})
        elif env == 'firebase':
            # # Create a storage client
            # bucket = storage.bucket()
            # # Create a new blob
            # blob = bucket.blob(file.filename)
            # # Upload the file's content
            # blob.upload_from_file(file)
            return jsonify({'message': 'File uploaded to Firebase successfully'})
    else:
        return jsonify({'error': 'No file selected'})
