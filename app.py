# CHECK THIS OUT FOR A CUSTOM ARTICLE ROUTING FUNCTION https://www.geeksforgeeks.org/flask-app-routing/
# IMPLEMENT WEBMANIFEST AND .ENV

from flask import *
from flask_login import *
from flask_wtf import *

app = Flask(__name__)
app.config.from_object("src.config") # Import configuration

# Enable anti Cross-site request forgery securiy
csrf = CSRFProtect(app)

# Initiate the login functionality
login_manager = LoginManager()
login_manager.init_app(app)

# Import all the proper models, alongside the sqlalchemy initiation
from src.models import db, Users

# Initiate the database
db.init_app(app)
with app.app_context():
    db.create_all()

# func to load in user
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

# Import all the site routes before starting the app, they are stored in the routes directory
import src.routes.login
import src.routes.articles
from src.routes.articles import titles, genProgressData, genChapterCompletion

"""The below code handles all the essential routes"""
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home/')
# @login_required talks with login manager to stop users from accesing the site when they aren't logged in
@login_required
def home():
    user = Users.query.filter_by(username=current_user.username).first() # Grab the users data by querying for their username
    
    return render_template('home.html', titles = titles, titles_keys = list(titles.keys()), progress_data = genProgressData(Users.query.filter_by(username=current_user.username).first()), completion_data = genChapterCompletion(Users.query.filter_by(username=current_user.username).first()))

@app.route('/progress/')
@login_required
def progress():
    user = Users.query.filter_by(username=current_user.username).first()
    
    return render_template('progress.html', titles = titles, titles_keys = list(titles.keys()), progress_data = genProgressData(Users.query.filter_by(username=current_user.username).first()), completion_data = genChapterCompletion(Users.query.filter_by(username=current_user.username).first()))

# logout
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("index"))

# Redirect to index when accessing part of site without proper unauthorization
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()