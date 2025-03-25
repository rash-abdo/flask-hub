from flask import (render_template,request,
                   redirect,url_for,flash)


def create_blog():
    if request.method == 'GET':
        return render_template('myblogs.html')