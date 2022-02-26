import os
import secrets
from PIL import Image
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import abort
from firewithinflims import app
from firewithinflims import db
from firewithinflims import bcrypt
from firewithinflims.forms import RegistrationForm
from firewithinflims.forms import UpdateAccountForm
from firewithinflims.forms import LoginForm
from firewithinflims.forms import PostForm
from firewithinflims.models import SUPost
from firewithinflims.models import SuperUser
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required


#   LANDING PAGE
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admindashboard'))
    return render_template('home.html')

#   ROUTE FOR ADMINS
@app.route('/admin/dashboard', methods=['GET', 'POST'])
@app.route('/admin/dashboard/', methods=['GET', 'POST'])
@login_required
def admindashboard():
    posts = SUPost.query.all()
    return render_template('dashboard.html', posts=posts)

#   VIEW INDIVIDUAL POST IN A SINGLE PAGE
@app.route("/admin/post/<int:post_id>")
@app.route("/admin/post/<int:post_id>/")
def adminpost(post_id):
    post = SUPost.query.get_or_404(post_id)
    image_file = url_for('static', filename='pictures/' + post.image_file)
    return render_template('post.html', title=post.title, post=post, image_file=image_file)

#   SAVE POST PICTURES
def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)

    output_size = (500, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#   UPDATE A POST 
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@app.route("/post/<int:post_id>/update/", methods=['GET', 'POST'])
@login_required
def adminupdate_post(post_id):
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
    return render_template('createpost.html', title='Update Post', image_file=image_file, form=form)


#   DELETE A POST
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@app.route("/post/<int:post_id>/delete/", methods=['POST'])
@login_required
def delete_post(post_id):
    post = SUPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('admindashboard'))

#   LO0GIN FOR ADMINS
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admindashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = SuperUser.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login success', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admindashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


#   ROUTE FOR LOGOUT
@app.route('/logout')
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


#   SAVE USER PROFILE PICTURES
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


#   ACCOUNT PAGE FOR ADMINS
@app.route('/admin/account', methods=['GET', 'POST'])
@app.route('/admin/account/', methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file)


#   ACCOUNT PAGE FOR ADMINS
@app.route('/admin/account/edit', methods=['GET', 'POST'])
@app.route('/admin/account/edit/', methods=['GET', 'POST'])
@login_required
def editaccount():
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
    return render_template('editaccount.html', title='Account', image_file=image_file, form=form)

#   ACCOUNT PAGE FOR ADMINS
@app.route('/post/create', methods=['GET', 'POST'])
@app.route('/post/create/', methods=['GET', 'POST'])
def createpost():
    form=PostForm()
    if form.validate_on_submit():
        post = SUPost(title=form.title.data,content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Success, your post is live now', 'success')
        return redirect(url_for('admindashboard'))
    return render_template('createpost.html', form=form)         

#   CREATE ACCOUNT FOR ADMIN
@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('admindashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = SuperUser(username=form.username.data, name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('admindashboard'))
    return render_template('signup.html', form=form)