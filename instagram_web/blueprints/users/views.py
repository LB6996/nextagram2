from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.image import Image
from flask_login import current_user,login_required
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
import datetime
import os



users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('users/sign_up.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    cfm_password = request.form.get('cfm_password')

    # if password == cfm_password:
    user = User(username=username, email=email, password=password, cfm_password=cfm_password)
    if user.save():
        flash('Successfully registered', 'alert alert-success')
        return redirect(url_for('home'))
    else:
        for error in user.errors:
            flash(error,'alert alert-danger')
        return render_template('users/sign_up.html')
    # else:
    #     flash('Password confirmation is not matching!','alert alert-danger')
    #     return render_template('users/sign_up.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):

    if current_user.is_authenticated:
        user = User.get_or_none(User.username == username)
        images = Image.select().where(Image.user==user.id)
        if user:
            return render_template('users/show.html',user=user,images=images)
        else:
            return render_template('404.html')  
    else:
        flash('Login required.','alert alert-danger')
        return render_template('sessions/login.html')

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if current_user == user:
        return render_template('users/edit.html')
    else:
        flash('Unauthorized to edit','alert alert-danger')
        return redirect(url_for('users.show',username=current_user.username))


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)
    if current_user == user:
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        if email != '':
            user.email = email
            user.password = None
        if first_name != '':
            user.first_name = first_name
            user.password = None
        if last_name != '':
            user.last_name = last_name
            user.password = None
        if password != '':
            user.password = password
        if user.save():
            flash('Profile updated successfully!','alert alert-success')
            return redirect(url_for('users.show',username=current_user.username))
        else:
            for error in user.errors:
                flash(error,'alert alert-danger')
            return redirect(url_for('home'))
    else: 
        flash('Unauthorized to edit','alert alert-danger')
        return redirect(url_for('users.show',username=current_user.username))



# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in os.getenv('ALLOWED_EXTENSIONS')

@users_blueprint.route('/upload', methods=['POST'])
def upload():

    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        flash('No user_file key in request.files','alert alert-danger')
        return redirect(url_for('users.edit',id=current_user.id))

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']

    # check whether a file is selected
    if file.filename == '':
        flash('No selected file','alert alert-danger')
        return redirect(url_for('users.edit',id=current_user.id))

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        file.filename = secure_filename(f"{str(datetime.datetime.now())}{file.filename}")
        output = upload_file_to_s3(file) 
        if output == file.filename:
            User.update(profile_image=output).where(User.id==current_user.id).execute()
            flash("Profile image successfully changed!","alert alert-success")
            return redirect(url_for('users.edit',id=current_user.id))
        else:
            flash("Image upload failed","alert alert-danger")
            return redirect(url_for('users.edit',id=current_user.id))

    # if file extension not allowed
    else:
        flash("File type not accepted,please try again.",'alert alert-danger')
        return redirect(url_for('users.edit',id=current_user.id))
