import os
import secrets
from PIL import Image
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import abort
from flask import current_app

from flask import Blueprint

from firewithinfilms import db
from firewithinfilms import bcrypt

from firewithinfilms.admin.forms import LoginForm
from firewithinfilms.admin.forms import PostForm
from firewithinfilms.admin.forms import UpdateAccountForm
from firewithinfilms.models import SUPost
from firewithinfilms.models import SuperUser

from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required

admin = Blueprint('admin', __name__)

#   SAVE USER PROFILE PICTURES
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#   ROUTE FOR ADMINS
@admin.route('/admin/dashboard', methods=['GET', 'POST'])
@admin.route('/admin/dashboard/', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    posts = SUPost.query.all()
    return render_template('admin/dashboard.html', posts=posts, scrolltop=True)

#   ACCOUNT PAGE FOR ADMINS
@admin.route('/admin/account', methods=['GET', 'POST'])
@admin.route('/admin/account/', methods=['GET', 'POST'])
@login_required
def admin_account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('admin/account.html', image_file=image_file)


#   ACCOUNT PAGE FOR ADMINS
@admin.route('/admin/account/edit', methods=['GET', 'POST'])
@admin.route('/admin/account/edit/', methods=['GET', 'POST'])
@login_required
def admin_edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            flash('successfully uploaded image', 'info')
        else:
            flash('NO image here', 'danger')
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('admin/editaccount.html', title='Account', image_file=image_file, form=form)  

#   VIEW INDIVIDUAL POST IN A SINGLE PAGE
@admin.route("/admin/post/<int:post_id>")
@admin.route("/admin/post/<int:post_id>/")
def admin_post(post_id):
    post = SUPost.query.get_or_404(post_id)
    image_file = url_for('static', filename='pictures/' + post.image_file)
    return render_template('admin/post.html', title=post.title, post=post, image_file=image_file)

#   SAVE POST PICTURES
def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pictures', picture_fn)

    output_size = (500, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#   ACCOUNT PAGE FOR ADMINS
@admin.route('/admin/post/create', methods=['GET', 'POST'])
@admin.route('/admin/post/create/', methods=['GET', 'POST'])
@login_required
def admin_create_post():
    form=PostForm()
    if form.validate_on_submit():
        picture_file = save_post_picture(form.picture.data)
        post = SUPost(title=form.title.data,content=form.content.data, author=current_user, image_file=picture_file)
        print(post)
        db.session.add(post)
        db.session.commit()
        flash('Success, your post is live now', 'success')
        return redirect(url_for('admindashboard'))
    return render_template('admin/createpost.html', form=form)   


#   UPDATE A POST 
@admin.route("/admin/post/<int:post_id>/update", methods=['GET', 'POST'])
@admin.route("/admin/post/<int:post_id>/update/", methods=['GET', 'POST'])
@login_required
def admin_update_post(post_id):
    post = SUPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('adminpost', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    image_file = url_for('static', filename='pictures/' + post.image_file)
    return render_template('admin/createpost.html', title='Update Post', image_file=image_file, form=form)


#   DELETE A POST
@admin.route("/admin/post/<int:post_id>/delete", methods=['POST'])
@admin.route("/admin/post/<int:post_id>/delete/", methods=['POST'])
@login_required
def admin_delete_post(post_id):
    post = SUPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('admindashboard'))    

#   LO0GIN FOR ADMINS
@admin.route('/youwillneverfind/login/', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = SuperUser.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login success', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin.admindashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin/login.html', form=form)


#   ROUTE FOR LOGOUT
@admin.route('/admin/logout')
@admin.route('/admin/logout/')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))