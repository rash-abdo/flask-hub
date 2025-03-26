from flask import (render_template,request,
                   redirect,url_for,flash,session)
from project.app import db
from project.blueprints.blogs.models import Blogs
import os
import datetime
import uuid


def create_blog():
    if request.method == 'GET':
        blogs_list = Blogs.query.filter_by(user_id=session['uid']).all()
        number_blogs = len(blogs_list)
        accending = sorted(blogs_list,key=lambda x: x.date,reverse=True)
        paths=[]
        dates=[]
        titles=[]
        for blog in accending:
            paths.append(blog.path)
            dates.append(blog.date)
            titles.append(blog.title)
        blogs=[]
        for path in paths:
            with open(path,'r') as f:
                blogs.append(f.read())
             
        

        return render_template('myblogs.html',paths=paths,blogs=blogs,
                               number_blogs=number_blogs,dates=dates,titles=titles)
    if request.method == 'POST':
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
        
        return redirect(url_for('blogs.create_blog'))