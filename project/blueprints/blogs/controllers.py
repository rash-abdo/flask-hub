from flask import (render_template,request,
                   redirect,url_for,flash,session)
from project.app import db
from project.blueprints.blogs.models import Blogs
from project.blueprints.profiles.models import Users,Info
import os
import datetime
import uuid



#view my blogs
def view_myblogs():
    user_id=session.get('uid')
    if not user_id:
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for('profile.logout'))
    
    blogs_list = Blogs.query.filter_by(user_id=user_id).all()
    number_blogs = len(blogs_list)
    blogs_list = sorted(blogs_list,key=lambda x: x.date,reverse=True)

    blogs=[]
    for blog in blogs_list:
        with open(blog.path,'r') as f:
            blogs.append(f.read())
            
    return render_template('myblogs.html',blogs_list=blogs_list,
                           blogs=blogs,number_blogs=number_blogs)

#create blog
def create_blog():
    
    title = request.form.get('title')
    blog = request.form.get('blog')
    path = f'project/uploads/blogs/Uid_{session["uid"]}'
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_name = uuid.uuid4().hex[:15]
    file = os.path.join(path,f'{file_name}.txt')

    if not os.path.exists(path):
        os.makedirs(path)
    with open(file,"w") as f:
        f.write(blog)

    blog = Blogs(date=time,path=file,
            user_id=session['uid'],title=title)
    db.session.add(blog)
    db.session.commit()
    
    return redirect(url_for('blogs.view_myblogs'))

#delete blog
def delete_blog(blog_id):
    blog = Blogs.query.get(blog_id)
    os.remove(blog.path)
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
        
        return render_template('edit_blog.html',title=title,
                               content=content,blog_id=blog_id)
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
    if request.method == 'GET':
        user_id=session.get('uid')
        blogs_list=Blogs.query.all()
        number_blogs = len(blogs_list)
        blogs_list = sorted(blogs_list,key=lambda x: x.date,reverse=True)

        users_name=[]
        for blog in blogs_list:
            users_name.append(Users.query.get(blog.user_id).name)
        
        blogs=[]
        for blog in blogs_list:
            with open(blog.path,'r') as f:
                blogs.append(f.read())
        
        return render_template('home.html',blogs_list=blogs_list,
                               blogs=blogs,number_blogs=number_blogs,
                               users_name=users_name)
    
#like function
def like(blog_id):
    blog = Blogs.query.get(blog_id)
    blog.like+=1
    db.session.commit()
    return redirect(url_for('blogs.home'))
#dislike function
def dislike(blog_id):
    blog = Blogs.query.get(blog_id)
    blog.dislike-=1
    db.session.commit()
    return redirect(url_for('blogs.home'))

#view other profiles
def other_profile(users_id):
    user = Users.query.get(users_id)
    info = Info.query.filter_by(user_id=users_id).first()

    email = user.email
    name = user.name
    color = info.color
    music = info.music

    blogs_list = Blogs.query.filter_by(user_id=users_id).all()
    number_blogs = len(blogs_list)
    blogs_list = sorted(blogs_list,key=lambda x: x.date,reverse=True)
    
    blogs=[]
    for blog in blogs_list:
        with open(blog.path,'r') as f:
            blogs.append(f.read())

    return render_template('other_profile.html',blogs_list=blogs_list,
                           blogs=blogs,number_blogs=number_blogs,
                        email=email,name=name,color=color,music=music)

