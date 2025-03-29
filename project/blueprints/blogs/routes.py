from project.blueprints.blogs.controllers import (delete_blog,create_blog,
                                                  view_myblogs,edit_blog,home,other_profile)
from flask import Blueprint


blogs = Blueprint('blogs',__name__,template_folder='templates')

blogs.add_url_rule('/home', 'home', home, methods=['GET'])
blogs.add_url_rule('/myblogs','view_myblogs',view_myblogs,methods=['GET','POST'])
blogs.add_url_rule('/delete blog','delete_blog',delete_blog,methods=['GET','POST'])
blogs.add_url_rule('/create blog','create_blog',create_blog,methods=['GET','POST'])
blogs.add_url_rule('/edit blog','edit_blog',edit_blog,methods=['GET','POST'])
blogs.add_url_rule('/<users_id>','other_profile',other_profile,methods=['GET','POST'])
