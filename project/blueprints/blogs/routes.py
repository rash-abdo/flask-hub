from project.blueprints.blogs.controllers import (create_blog)
from flask import Blueprint


blogs = Blueprint('blogs',__name__,template_folder='templates')
blogs.add_url_rule('/myblogs','create_blog',create_blog,methods=['GET','POST'])