from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import false
from .models import Post, Comment, Like, Reply
from . import db

views = Blueprint("views", __name__)


#this route is for home page where all posts will be visible
@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user = current_user, posts = posts)


@views.route("/create_post", methods = ['GET', 'POST'])
@login_required
def createPost():
    if request.method == 'POST':
        post_title = request.form.get('blog_title')
        post_content = request.form.get('blog_content')

        if post_content:                                    
            #print(post_content)
            post = Post(title = post_title, content = post_content, author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('post created', category='success')
            redirect(url_for('views.home'))
        else:
            flash('post content cannot be empty', category='error')

    return render_template("create_post2.html", user = current_user)


@views.route("/delete_post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id = id).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif current_user.id != post.author:
        flash('You dont have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category = 'success')
    
    return redirect(url_for('views.home'))


@views.route("/posts/<user_id>")
@login_required
def display_all_post(user_id):
    posts = Post.query.filter_by(author = user_id).all()

    #logic to get user name of the clicked post
    first_post_of_user = Post.query.filter_by(author = user_id).first()
    username = first_post_of_user.user.username

    return render_template('posts.html', user = current_user, posts = posts, username = username)

@views.route("/view_post/<post_id>")
@login_required
def display_full_post(post_id):
    post = Post.query.filter_by(id = post_id).first()

    return render_template('view_post.html', user = current_user, post = post)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        flash('Post does not exists', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route("/create-reply/<post_id>/<comment_id>", methods=['POST'])
@login_required
def create_reply(post_id, comment_id):

    reply_text = request.form.get('reply')

    if not reply_text:
        flash('Reply cannot be empty', category='error')
    else:
        reply = Reply(text = reply_text, author = current_user.id, post_id = post_id, comment_id = comment_id)
        db.session.add(reply)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route("/delete-reply/<reply_id>")
@login_required
def delete_reply(reply_id):

    reply = Reply.query.filter_by(id = reply_id).first()

    if not reply:
        flash('Reply does not exists!', category='error')
    else:
        db.session.delete(reply)
        db.session.commit()

    return redirect(url_for('views.home'))
