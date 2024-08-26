from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import jinja2 

# Initialize Flask app and configure settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Tyler\\flask_app\\lifting_log\\lifting_log.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'alskdjfasdfasdfkljasgjalsdfkgj' 

# Setup Jinja2 environment and add 'zip' to global context for templates
env = jinja2.Environment()
app.jinja_env.globals.update(zip=zip)

# Setup Flask-Login for session management
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

# Initialize database and migration support
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes from views.py after app initialization
from views import *

# Run the Flask development server
if __name__ == '__main__':
	app.run()