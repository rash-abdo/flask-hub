from project.app import db,bcrypt
from flask import (redirect,render_template,
                   request,session,flash,url_for)
from project.blueprints.profiles.models import Users,Info

#view home page
def index():
    if request.method == 'GET':
        return render_template('home.html')


#view user profile function
def user_profile():
    if request.method == 'GET':
        try:
            user = Users.query.get(session['uid'])
            info = Info.query.filter_by(user_id=session['uid']).first()
                        
            name = user.name
            email = user.email
            color = info.color
            music = info.music
            
            return render_template('user_profile.html',name=name,
                        email=email,color=color,music=music)
        except KeyError:
            return redirect(url_for('profile.logout'))
        

#logout function
def logout():
    session.pop('uid',None)
    return render_template('logout.html')


#delete profile function
def delete():
    user = Users.query.get(session['uid'])
    info = Info.query.filter_by(user_id=session['uid']).first()
    db.session.delete(info)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('profile.logout'))


#login function
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password,password):
                session['uid'] = user.id               
                return redirect(url_for('profile.index'))
            else:
                flash('incorrect password')
                return render_template('login.html')
        else:
            flash('there is no such email')
            return render_template('login.html')


#sign up function
def sign_up():
    if request.method == 'GET':
        return render_template('sign.html')
    elif request.method == 'POST':
        user = Users()
        email = Users.query.filter_by(email=request.form.get('email')).first()
        hashed_password = bcrypt.generate_password_hash(request.form.get('password'))        
        password = Users.query.filter_by(password=hashed_password).first()
        if email and password:
            flash('email is taken')
            flash('password is taken')
            return render_template('sign.html')
        elif email:
            flash('email is taken')
            return render_template('sign.html')
        elif password:
            flash('password is taken')
            return render_template('sign.html')
        else:

            
            user = Users(name=request.form.get('name'),
            email=request.form.get('email'),
            password=hashed_password)
            db.session.add(user)
            db.session.commit()
            
            info = Info(user_id = user.id ,color=None,music=None)
            db.session.add(info)
            db.session.commit()
            session['uid'] = user.id
            return redirect(url_for('profile.index'))
        

#edit profile information function
def edit():
    if request.method == 'GET':
        user = Users.query.get(session['uid'])
        info = Info.query.filter_by(user_id=session['uid']).first()
        
        name = user.name
        email = user.email
        color = info.color
        music = info.music
        
        return render_template('edit.html',name=name,
                    email=email,color=color,music=music)
        
    if request.method == 'POST':
        user = Users.query.get(session['uid'])
        info = Info.query.filter_by(user_id=session['uid']).first()
        
        new_name = request.form.get('name')
        new_email = request.form.get('email')
        new_color = request.form.get('color')
        new_music = request.form.get('music')
        
        user.name = new_name
        info.color = new_color
        info.music = new_music
        if new_email == user.email or len(Users.query.filter_by(email=new_email).all())==0:
            user.email = new_email
        else:
            flash('email is taken')
        db.session.commit()
        return redirect(url_for('profile.user_profile'))
        

#change password function        
def change_password():
    if request.method == 'GET':
        print('asdasd')
        return render_template('change_password.html')
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        user = Users.query.get(session['uid'])
        
        if bcrypt.check_password_hash(user.password,old_password):
            new_pass_hash = bcrypt.generate_password_hash(new_password)
            known = Users.query.filter_by(password=new_pass_hash).first()
            if known:
                flash('new password is Tacken')

            else:
                user.password = new_pass_hash
                db.session.commit()
                flash('password changed succesfully')
        else:
            flash('wrong password')
        
        return redirect(url_for('profile.user_profile'))
        