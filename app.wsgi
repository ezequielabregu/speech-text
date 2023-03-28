#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/flask_app')

from app import app as application