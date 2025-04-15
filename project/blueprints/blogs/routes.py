from project.blueprints.blogs.controllers import (delete_blog,create_blog,
                                                  view_myblogs,edit_blog,home,other_profile,
                                                  like,dislike)
from flask import Blueprint


blogs = Blueprint('blogs',__name__,template_folder='templates', static_folder='static',static_url_path='/')

blogs.add_url_rule('/', 'home', home, methods=['GET'])
blogs.add_url_rule('/myblogs','view_myblogs',view_myblogs,methods=['GET','POST'])
blogs.add_url_rule('/delete blog/<blog_id>','delete_blog',delete_blog,methods=['GET','POST'])
blogs.add_url_rule('/create blog','create_blog',create_blog,methods=['GET','POST'])
blogs.add_url_rule('/edit blog/<blog_id>','edit_blog',edit_blog,methods=['GET','POST'])
blogs.add_url_rule('/<users_id>','other_profile',other_profile,methods=['GET','POST'])
blogs.add_url_rule('/dislike/<blog_id>','dislike',dislike,methods=['POST'])
blogs.add_url_rule('/like/<blog_id>','like',like,methods=['POST'])
