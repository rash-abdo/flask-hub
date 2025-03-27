from project.blueprints.blogs.controllers import (myblogs,edit_blog)
from flask import Blueprint


blogs = Blueprint('blogs',__name__,template_folder='templates')
blogs.add_url_rule('/myblogs','myblogs',myblogs,methods=['GET','POST'])
blogs.add_url_rule('/edit blog','edit_blog',edit_blog,methods=['GET','POST'])
