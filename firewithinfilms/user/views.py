import os
import re
import secrets
from PIL import Image

from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import session
from flask import abort
from flask import current_app

from flask import Blueprint

from firewithinfilms import db
from firewithinfilms import bcrypt

from firewithinfilms.user.forms import RegistrationForm
from firewithinfilms.user.forms import LoginForm
from firewithinfilms.user.forms import UpdateAccountForm
from firewithinfilms.user.forms import UpdateAccountDescriptionForm
from firewithinfilms.user.forms import PostForm

from firewithinfilms.models import User
from firewithinfilms.models import UserPost
from firewithinfilms.models import UserDetails
from firewithinfilms.models import UserReviews

from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required

from firewithinfilms.save_image import save_post_picture
from firewithinfilms.save_image import save_profile_picture


user = Blueprint('users', __name__)

# USER PUBLIC PROFLE
@user.route('/<string:username>/')
def user_profile(username):
    return f"This page is underconstraction, but the username is {username}"

#   DASHBOARD FOR USER
@user.route('/user/dashboard/', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    # posts = UserPost.query.all()
    posts = UserPost.query.order_by(UserPost.date_posted.desc()).all()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    reviews = UserReviews.query.filter_by(user_id=user.id)
    details = UserDetails.query.filter_by(user_id=user.id)
    completed_account_descreption=False
    complete_account=False
    for detail in details:
        if detail.user_headline == 'N/A': 
            completed_account_descreption=False
            print('User headline is NA')
        else:
            completed_account_descreption=True
            print('User headline is GOOD')

        if detail.description == 'N/A':
            completed_account_descreption=False
            print('User description is NA')
        else:
            completed_account_descreption=True
            print('User description is GOOD')
        
        if detail.primary_lang == 'N/A':
            completed_account_descreption=False
            print('User primary_lang is NA')
        else:
            completed_account_descreption=True
            print('User primary_lang is GOOD')
        
        if detail.secondary_lang == 'N/A':
            completed_account_descreption=False
            print('User secondary_lang is NA')
        else:
            completed_account_descreption=True
            print('User secondary_lang is GOOD')
        
        if detail.skill_1 == 'N/A':
            completed_account_descreption=False
            print('User skill_1 is NA')
        else:
            completed_account_descreption=True
            print('User skill_1 is GOOD')
        
        if detail.skill_2 == 'N/A':
            completed_account_descreption=False
            print('User skill_2 is NA')
        else:
            completed_account_descreption=True
            print('User skill_2 is GOOD')
        
        if detail.skill_3 == 'N/A':
            completed_account_descreption=False
            print('User skill_3 is NA')
        else:
            completed_account_descreption=True
            print('User skill_3 is GOOD')
        
        if detail.skill_4 == 'N/A':
            completed_account_descreption=False
            print('User skill_4 is NA')
        else:
            completed_account_descreption=True
            print('User skill_4 is GOOD')
        
        if detail.skill_5 == 'N/A':
            completed_account_descreption=False
            print('User skill_5 is NA')
        else:
            completed_account_descreption=True
            print('User skill_5 is GOOD')
        
        if detail.education_institue_name == 'N/A':
            completed_account_descreption=False
            print('User education_graduation_name is NA')
        else:
            completed_account_descreption=True
            print('User education_graduation_name is GOOD')
        
        if detail.education_graduation_name == 'N/A':
            completed_account_descreption=False
            print('User education_graduation_name is NA')
        else:
            completed_account_descreption=True
            print('User education_graduation_name is GOOD')
        
        if detail.education_institue_country == 'N/A':
            completed_account_descreption=False
            print('User education_institue_country is NA')
        else:
            completed_account_descreption=True
            print('User education_institue_country is GOOD')
        
        if user.name == None:
            print('name is none')
            complete_account=False   
        else:
            print('name is something')
            complete_account=True

    return render_template('user/dashboard.html', posts=posts, completed_account_descreption=completed_account_descreption, 
                        complete_account=complete_account)

#   ACCOUNT PAGE FOR USERS
@user.route('/user/account/', methods=['GET', 'POST'])
@login_required
def user_account():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        reviews = UserReviews.query.filter_by(user_id=user.id)
        details = UserDetails.query.filter_by(user_id=user.id)

        review_1 = 0
        review_2 = 0
        review_3 = 0
        review_4 = 0
        review_5 = 0
        avg_review_counting = 0
        remainder=0
        null_review = True

        # counting review
        for review in reviews:
            print('-------------')
            print(f'Review---->>> {review.star}')
            if review.star != '0':
                avg_review_counting = avg_review_counting+int(review.star)
                remainder += 1
                null_review = False
        
            if review.star == '5':
                review_5 = review_5 + 1
            elif review.star == '4':
                review_4 = review_4 + 1
            elif review.star == '3':
                review_3 = review_3 + 1
            elif review.star == '2':
                review_2 = review_2 + 1
            elif review.star == '1':
                review_1 = review_1 + 1
            else:
                null_review=True

        # average review
        if null_review == True:
            avg_review=0
        else:
            avg_review = avg_review_counting/remainder
    

        # checking if the user profile is complete
        for detail in details:
            if detail.user_headline == 'N/A': 
                completed_account_descreption=False
                print('User headline is NA')
            else:
                completed_account_descreption=True
                print('User headline is GOOD')

            if detail.description == 'N/A':
                completed_account_descreption=False
                print('User description is NA')
            else:
                completed_account_descreption=True
                print('User description is GOOD')
            
            if detail.primary_lang == 'N/A':
                completed_account_descreption=False
                print('User primary_lang is NA')
            else:
                completed_account_descreption=True
                print('User primary_lang is GOOD')
            
            if detail.secondary_lang == 'N/A':
                completed_account_descreption=False
                print('User secondary_lang is NA')
            else:
                completed_account_descreption=True
                print('User secondary_lang is GOOD')
            
            if detail.skill_1 == 'N/A':
                completed_account_descreption=False
                print('User skill_1 is NA')
            else:
                completed_account_descreption=True
                print('User skill_1 is GOOD')
            
            if detail.skill_2 == 'N/A':
                completed_account_descreption=False
                print('User skill_2 is NA')
            else:
                completed_account_descreption=True
                print('User skill_2 is GOOD')
            
            if detail.skill_3 == 'N/A':
                completed_account_descreption=False
                print('User skill_3 is NA')
            else:
                completed_account_descreption=True
                print('User skill_3 is GOOD')
            
            if detail.skill_4 == 'N/A':
                completed_account_descreption=False
                print('User skill_4 is NA')
            else:
                completed_account_descreption=True
                print('User skill_4 is GOOD')
            
            if detail.skill_5 == 'N/A':
                completed_account_descreption=False
                print('User skill_5 is NA')
            else:
                completed_account_descreption=True
                print('User skill_5 is GOOD')
            
            if detail.education_institue_name == 'N/A':
                completed_account_descreption=False
                print('User education_graduation_name is NA')
            else:
                completed_account_descreption=True
                print('User education_graduation_name is GOOD')
            
            if detail.education_graduation_name == 'N/A':
                completed_account_descreption=False
                print('User education_graduation_name is NA')
            else:
                completed_account_descreption=True
                print('User education_graduation_name is GOOD')
            
            if detail.education_institue_country == 'N/A':
                completed_account_descreption=False
                print('User education_institue_country is NA')
            else:
                completed_account_descreption=True
                print('User education_institue_country is GOOD')

            # print(f'--------->> is profile completed? >>>> {completed_account_descreption}')
            # print(f'User headline: {detail.user_headline}')
            # print(f'country: {detail.country}')
            # print(f'Details: {detail.description}')
            # print(f'Primary Language: {detail.primary_lang}')
            # print(f'Secondary Language: {detail.secondary_lang}')
            # print(f'Skill 1: {detail.skill_1}')
            # print(f'SKill 2: {detail.skill_2}')
            # print(f'SKill 3: {detail.skill_3}')
            # print(f'SKill 4: {detail.skill_4}')
            # print(f'SKill 5: {detail.skill_5}')
            # print(f'Education institute name: {detail.education_institue_name}') 
            # print(f'Education gradutation name: {detail.education_graduation_name}')
            # print(f'Education institute country: {detail.education_institue_country}')
            
            if user.name == None:
                print('name is none')
                complete_account=False   
            else:
                print('name is something')
                complete_account=True

        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
        return render_template('user/account.html', image_file=image_file, details=details,
                review_5=review_5, review_4=review_4, review_3=review_3, review_2=review_2, review_1=review_1, avg_review=round(avg_review,2),
                completed_account_descreption=completed_account_descreption, complete_account=complete_account)

    return redirect(user.user_login)

#   ACCOUNT PAGE FOR ADMINS
@user.route('/user/account/edit/', methods=['GET', 'POST'])
@login_required
def user_edit_account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.user_account'))
    
    if request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user/editaccount.html', title='Account', image_file=image_file, form=form)  


#   ACCOUNT PAGE FOR ADMINS
@user.route('/user/account/description/edit/', methods=['GET', 'POST'])
@login_required
def user_edit_description():
    # query data from database
    form = UpdateAccountDescriptionForm()
    details = UserDetails.query.all()

    if form.validate_on_submit():
        for detail in details:
            detail.description = form.description.data
            detail.primary_lang = form.primary_lang.data
            detail.secondary_lang = form.secondary_lang.data
            detail.skill_1 = form.skill_1.data
            detail.skill_2 = form.skill_2.data
            detail.skill_3 = form.skill_3.data       
            detail.skill_4 = form.skill_4.data
            detail.skill_5 = form.skill_5.data  
            detail.education_institue_name = form.education_institue_name.data
            detail.education_institue_country = form.education_institue_country.data
            detail.education_graduation_name = form.education_graduation_name.data
            detail.education_graduation_year = form.education_graduation_year.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.user_account'))    
    if request.method == 'GET':
        for detail in details:
            form.description.data = detail.description
            form.primary_lang.data = detail.primary_lang
            form.secondary_lang.data = detail.secondary_lang
            form.skill_1.data = detail.skill_1
            form.skill_2.data = detail.skill_2
            form.skill_3.data = detail.skill_3        
            form.skill_4.data = detail.skill_4
            form.skill_5.data = detail.skill_5
            form.education_institue_name.data = detail.education_institue_name
            form.education_institue_country.data = detail.education_institue_country
            form.education_graduation_name.data = detail.education_graduation_name
            if detail.education_graduation_year == '0':
                form.education_graduation_year.data = 'Currently Studying'
            form.education_graduation_year.data = detail.education_graduation_year
   
    return render_template(
        'user/editaccount_description.html', title="Edit Account Description", form=form)


#   INBOX FOR USERS
@user.route('/user/inbox/', methods=['GET', 'POST'])
@login_required
def user_inbox():
    return "Sorry for your inconvinience, but this page is under constraction"

    
#   VIEW INDIVIDUAL POST IN A SINGLE PAGE
@user.route("/user/post/<int:post_id>/")
def user_post(post_id):
    post = UserPost.query.get_or_404(post_id)
    post_author_details = UserDetails.query.filter_by(user_id=post.author.id)
    author_all_post = UserPost.query.filter_by(user_id=post.author.id).order_by(UserPost.date_posted.desc()).paginate(1, 3, False).items
    print('======= author all post =============')
    for author_post in author_all_post:
        print(author_post)
        print(author_post.id) 
    print('====================')

    # query suggest blog post with pagination
    # post_query = UserPost.query.paginate(1, 4, False)
    # suggest_post_author = post_query.items
    post_query = UserPost.query.order_by(UserPost.date_posted.desc()).paginate(1, 4, False)
    suggest_post_author = post_query.items

    # find last post
    lastPost = UserPost.query.order_by(UserPost.date_posted.desc()).first()

    print('======= suggested post author =============')
    print(suggest_post_author)
    for author in suggest_post_author:
        print(author.author.name)
    print('====================')
    

    if post.image_file:
        image_file = url_for('static', filename='pictures/' + post.image_file)
        image_file_status = True
        print(f'image url is {image_file}')
        print(f'image is {post.image_file}')

        return render_template('user/post.html', title=post.title, post=post, image_file=image_file, image_file_status=image_file_status, post_author_details=post_author_details, author_all_post=author_all_post, suggest_post_author=suggest_post_author, lastPost=lastPost)
    else:
        image_file_status = False

    return render_template('user/post.html', title=post.title, post=post, image_file_status=image_file_status, post_author_details=post_author_details,author_all_post=author_all_post, suggest_post_author=suggest_post_author, lastPost=lastPost)

#   CREATE POST
@user.route('/post/create/', methods=['GET', 'POST'])
@login_required
def user_create_post():
    form=PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            post = UserPost(title=form.title.data,content=form.content.data, author=current_user, image_file=picture_file)
        else:
            post = UserPost(title=form.title.data,content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Success, your post is live now', 'success')
        return redirect(url_for('users.user_dashboard'))
    return render_template('user/createpost.html', form=form)   


#   UPDATE A POST 
@user.route("/user/post/<int:post_id>/update/", methods=['GET', 'POST'])
@login_required
def user_update_post(post_id):
    post = UserPost.query.get_or_404(post_id)
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
        return redirect(url_for('users.user_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    image_file = url_for('static', filename='pictures/' + post.image_file)
    return render_template('user/createpost.html', title='Update Post', image_file=image_file, form=form)


#   DELETE A POST
@user.route("/user/post/<int:post_id>/delete/", methods=['POST'])
@login_required
def user_delete_post(post_id):
    post = UserPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.user_dashboard'))    

#   CREATE ACCOUNT FOR USER
@user.route('/signup/', methods=['GET', 'POST'])
def user_signup():
    if current_user.is_authenticated:
        return redirect(url_for('users.user_dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user_detail = User.query.filter_by(email=form.email.data).first()
        reviews = UserReviews(user_id=user_detail.id)
        details = UserDetails(user_id=user_detail.id)
        db.session.add(reviews)
        db.session.add(details)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.user_login'))

    return render_template('user/signup.html', form=form)


#   LO0GIN FOR USER
@user.route('/login/', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('users.user_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.user_role!='admin':
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login success', 'success')
            return redirect(next_page) if next_page else redirect(url_for('users.user_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', form=form)


#   LOGOUT FOR USER
@user.route("/logout/")
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('users.user_login'))