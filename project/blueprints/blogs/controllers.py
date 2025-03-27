from flask import (render_template,request,
                   redirect,url_for,flash,session)
from project.app import db
from project.blueprints.blogs.models import Blogs
import os
import datetime
import uuid


def view_myblogs():
    blogs_list = Blogs.query.filter_by(user_id=session['uid']).all()
    number_blogs = len(blogs_list)
    accending = sorted(blogs_list,key=lambda x: x.date,reverse=True)
    paths=[]
    dates=[]
    titles=[]
    blog_ids=[]
    for blog in accending:
        blog_ids.append(blog.id)
        paths.append(blog.path)
        dates.append(blog.date)
        titles.append(blog.title)
    blogs=[]
    for path in paths:
        with open(path,'r') as f:
            blogs.append(f.read())
             
    return render_template('myblogs.html',paths=paths,blogs=blogs,
                           number_blogs=number_blogs,dates=dates,
                           titles=titles,blog_ids=blog_ids)
    
def create_blog():
    
    title = request.form.get('title')
    blog = request.form.get('blog')
    path = f'project/uploads/blogs/Uid_{session["uid"]}'
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_name = uuid.uuid4().hex[:15]
    file = f'{path}/{file_name}.txt'

    if not os.path.exists(path):
        os.makedirs(path)
    with open(file,"w") as f:
        f.write(blog)

    blog = Blogs(date=time,path=file,
            user_id=session['uid'],title=title)
    db.session.add(blog)
    db.session.commit()
    
    return redirect(url_for('blogs.myblogs'))

def delete_blog():
    blog_id=int(request.form.get('blog_id'))
    blog = Blogs.query.get(blog_id)
    os.remove(blog.path)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('blogs.myblogs'))

def edit_blog():
    if request.method=='GET':
        blog_id=int(request.args.get('blog_id'))
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

        return redirect(url_for('blogs.myblogs'))

def myblogs():
    action = request.form.get('action')
    if request.method == 'GET':
        return view_myblogs()
    if request.method == 'POST' and action == 'create':
        return create_blog()
    if request.method == 'POST' and action == 'delete':
        return delete_blog()