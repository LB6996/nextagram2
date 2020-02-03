from flask import Blueprint, render_template, request, flash, redirect, url_for
from instagram_web.util.helpers import upload_file_to_s3
from flask_login import current_user
from models.user import User
from models.image import Image
from werkzeug.utils import secure_filename
import datetime



images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
def new():
    pass

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@images_blueprint.route('/create', methods=['POST'])
def upload():
    if 'user_file' not in request.files:
        flash('no user_file key in request.files','alert alert-danger')
        return redirect(url_for('users.edit',id=current_user.id))

    file = request.files['user_file']

    if file.filename == '':
        flash('No selected file','alert alert-danger')
        return redirect(url_for('users.edit',id=current_user.id))
    
    if file and allowed_file(file.filename):
        file.filename = secure_filename(f"{str(datetime.datetime.now())}{file.filename}")
        output = upload_file_to_s3(file)
        if output:
            flash('Image successfully uploaded!','alert alert-success')
            image = Image(user=current_user.id,image_path=file.filename)
            image.save()
            return redirect(url_for('users.edit',id=current_user.id))
        else:
            flash('Image upload failed','alert alert-danger')
            return redirect(url_for('users.edit',id=current_user.id))
    else:
        flash('File type not accepted, please try again.','alert alert-danger')
        return redirect(url_for('users.edit',id=current_user.id))
@images_blueprint.route('/<username>', methods=['GET'])
def show():
    pass

@images_blueprint.route('/<username>/destroy', methods=['POST'])
def destroy():
    pass


