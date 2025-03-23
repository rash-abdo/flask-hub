from flask import Blueprint
from project.blueprints.profiles.controllers import (index,user_profile,login,logout,
                      delete,edit,sign_up,change_password)


profile = Blueprint('profile', __name__,template_folder='templates')

profile.add_url_rule('/home', 'index', index, methods=['GET'])
profile.add_url_rule('/user_profile', 'user_profile', user_profile, methods=['GET', 'POST'])
profile.add_url_rule('/logout', 'logout', logout, methods=['GET'])
profile.add_url_rule('/delete', 'delete', delete, methods=['GET'])
profile.add_url_rule('/edit', 'edit', edit, methods=['GET', 'POST'])
profile.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
profile.add_url_rule('/sign_up', 'sign_up', sign_up, methods=['GET', 'POST'])
profile.add_url_rule('/change_password','change_password',change_password,methods=['GET','POST'])