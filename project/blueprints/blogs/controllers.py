from flask import (render_template,request,
                   redirect,url_for,flash,session)
from project.app import db
from project.blueprints.blogs.models import Blogs
import os
import datetime


def create_blog():
    if request.method == 'GET':
        return render_template('myblogs.html')
    if request.method == 'POST':
        title = request.form.get('title')
        blog = request.form.get('blog')
        if not os.path.exists(f'project/uploads/blogs/Uid_{session["uid"]}'):
            os.makedirs(f'project/uploads/blogs/Uid_{session["uid"]}')
        with open(f'project/uploads/blogs/Uid_{session["uid"]}/{title}.txt',"w") as f:
            f.write(blog)
        
        return redirect(url_for('blogs.create_blog'))