from flask import (render_template,request,send_from_directory,current_app,
                   redirect,url_for,flash,session,send_file)
from project.app import db
from project.blueprints.blogs.models import Blogs,Likes,Comments
from project.blueprints.profiles.models import Users,Info
import os
import datetime
import uuid
from werkzeug.utils import secure_filename
from sqlalchemy.exc import DataError


#view my blogs
def view_myblogs():
    user_id=session.get('uid')
    if not user_id:
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for('profile.logout'))
    
    blogs_list = Blogs.query.filter_by(user_id=user_id).all()
    blogs_list = sorted(blogs_list,key=lambda x: x.date,reverse=True)

    blogs=[]
    for blog in blogs_list:
        with open(blog.path,'r') as f:
            blogs.append(f.read())
            
    return render_template('myblogs.html',blogs_list=blogs_list,
                           blogs=blogs)

#view image
def view_image(path):
    return send_file(path)

#create blog
def create_blog():
    
    title = request.form.get('title')
    blog = request.form.get('blog')
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    path = f'{current_app.config['UPLOAD_FOLDER']}/blogs/Uid_{session["uid"]}'

    file_name = uuid.uuid4().hex[:15]
    file = os.path.join(path,f'{file_name}.txt')

    if not os.path.exists(path):
        os.makedirs(path)
    with open(file,"w") as f:
        f.write(blog)
    
    image_path = None
    image = request.files.get('image')
    if image:
        path = current_app.config['UPLOAD_IMAGE_FOLDER']
        if not os.path.exists(path):
            os.makedirs(path)
        ext = os.path.splitext(image.filename)[1].lower()
        image_filename = secure_filename(uuid.uuid4().hex + ext)

        image_path = os.path.join(path, image_filename)
        image.save(image_path)
        image_path = os.path.abspath(image_path)
        
    blog = Blogs(date=time,path=file,
            user_id=session['uid'],title=title,image=image_path)
    db.session.add(blog)
    db.session.commit()
    
    return redirect(url_for('blogs.view_myblogs'))

#delete blog
def delete_blog(blog_id):
    blog = Blogs.query.get(blog_id)
    os.remove(blog.path)
    os.remove(blog.image)
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('blogs.view_myblogs'))

#edit blog
def edit_blog(blog_id):
    if request.method=='GET':
        blog = Blogs.query.get(blog_id)
        title=blog.title
        with open(blog.path,'r') as f:
            content=f.read()
        
        return render_template('edit_blog.html',blog=blog,
                               content=content)
    if request.method=='POST':
        new_title = request.form.get('title')
        new_blog = request.form.get('blog')
        blog_id=int(request.form.get('blog_id'))
        blog = Blogs.query.get(blog_id)

        blog.title=new_title
        db.session.commit()
        with open(blog.path,'w') as f:
            f.write(new_blog)

        return redirect(url_for('blogs.view_myblogs'))
    
#view home page
def home():
    user_id=session.get('uid')
    blogs_list=Blogs.query.all()
    blogs_list = sorted(blogs_list,key=lambda x: x.date,reverse=True)

    users_name=[]
    for blog in blogs_list:
        users_name.append(Users.query.get(blog.user_id).name)
    
    blogs_contents=[]
    for blog in blogs_list:
        with open(blog.path,'r') as f:
            blogs_contents.append(f.read())
    
    likes=[]
    if user_id:
        likes = Likes.query.filter_by(user_id=user_id).all()

    return render_template('home.html',blogs_list=blogs_list,
                           blogs_contents=blogs_contents,
                           users_name=users_name,
                           likes_json=[like.to_dict() for like in likes])

#view other profiles
def other_profile(users_id):
    user_id=session.get('uid')
    user = Users.query.get(users_id)
    info = Info.query.filter_by(user_id=users_id).first()

    email = user.email
    name = user.name
    color = info.color
    music = info.music

    blogs_list = Blogs.query.filter_by(user_id=users_id).all()
    blogs_list = sorted(blogs_list,key=lambda x: x.date,reverse=True)
    
    blogs_contents=[]
    for blog in blogs_list:
        with open(blog.path,'r') as f:
            blogs_contents.append(f.read())
    
    if user_id:
        likes = Likes.query.filter_by(user_id=user_id).all()

    return render_template('other_profile.html',blogs_list=blogs_list,
                           blogs_contents=blogs_contents,
                        email=email,name=name,color=color,music=music,
                        likes_json=[like.to_dict() for like in likes])

#like function
def like(blog_id):
    user_id = session.get('uid')
    if user_id:
        like = Likes.query.filter_by(blog_id=blog_id,user_id=user_id).first()
        blog = Blogs.query.get(blog_id)
        if not like:
            like = Likes(blog_id=blog_id, user_id=user_id, likes=1)
            blog.likes+=1
            db.session.add(like)
            db.session.commit()
        else:
            if like.likes:
                blog.likes-=1
                db.session.delete(like)
                db.session.commit()
            else:
                blog.likes+=1
                blog.dislikes+=1
                like.likes = 1
                db.session.commit()
        return redirect(request.referrer)
    else:
        return redirect(url_for('profile.logout'))
#dislike function
def dislike(blog_id):
    user_id = session.get('uid')
    if user_id:
        like = Likes.query.filter_by(blog_id=blog_id,user_id=user_id).first()
        blog = Blogs.query.get(blog_id)
        if not like:
            like = Likes(blog_id=blog_id, user_id=user_id, likes=0)
            blog.dislikes-=1
            db.session.add(like)
            db.session.commit()
        else:
            if like.likes:
                blog.likes-=1
                blog.dislikes-=1
                like.likes = 0
                db.session.commit()
            else:
                blog.dislikes+=1
                db.session.delete(like)
                db.session.commit()
        return redirect(request.referrer)
    else:
        return redirect(url_for('profile.logout'))

#add comment function
def comment(blog_id):
    user_id = session.get('uid')
    if user_id:
        try:
            blog = Blogs.query.get(blog_id)
            
            content = request.form.get('comment')
            comment = Comments(blog_id=blog_id,user_id=user_id,comment=content)
            blog.comments+=1
            
            db.session.add(comment)
            db.session.commit()
            return redirect(request.referrer)
        except DataError:
            flash("Your comment is too long", "warning")
            db.session.rollback()
            return redirect(request.referrer)
    else:
        return redirect(url_for('profile.logout'))

#view comments function
def view_comments(blog_id):
    user_id = session.get('uid')
    blog = Blogs.query.get(blog_id)
    user_name = Users.query.get(blog.user_id).name

    with open(blog.path,'r') as f:
        blog_content = f.read()


    likes=[]
    if user_id:
        likes = Likes.query.filter_by(user_id=user_id).all()
    
    comments = Comments.query.filter_by(blog_id=blog_id)
    users_names=[]
    for comment in comments:
        name = Users.query.get(comment.user_id).name
        users_names.append(name)
    
    return render_template('comments.html',users_names=users_names,
                           blog_content=blog_content,comments=comments,
                           user_name=user_name,blog=blog,user_id=user_id,
                           likes_json = [like.to_dict() for like in likes])

#delete comment function
def delete_comment(comment_id):
    comment = Comments.query.get(comment_id)
    blog = Blogs.query.get(comment.blog_id)
    db.session.delete(comment)
    blog.comments-=1
    db.session.commit()
    return redirect(request.referrer)