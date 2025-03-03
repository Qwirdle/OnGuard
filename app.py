# If you can't understand this codebase, it's your own fault <3 - Jasper

# maybe, transfer all summary stuff into summary category, not necessary though

from flask import *
from flask_login import *
from flask_wtf import *
import os
import datetime

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
from src.routes.articles import titles, genProgressData, genChapterCompletion, excludeList, courseCompleted, autoComplete
from src.cert import genCert

"""The below code handles all the essential routes"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home/')
# @login_required talks with login manager to stop users from accesing the site when they aren't logged in
@login_required
def home():
    user = Users.query.filter_by(username=current_user.username).first() # Grab the users data by querying for their username
    # autoComplete(user) # FOR DEBUG PURPOSES, COMMENT OUT ON DEPLOYMENT
    
    # check for completion
    if user.cdate == "none" and courseCompleted(user):
                # normal date formatting
                user.cdate = datetime.datetime.now().strftime("%B %d, %Y")

    return render_template('home.html', titles = titles, title = "Home", titles_keys = list(titles.keys()), progress_data = genProgressData(Users.query.filter_by(username=current_user.username).first()), completion_data = genChapterCompletion(Users.query.filter_by(username=current_user.username).first()), excludeTitle = False, courseComplete = courseCompleted(user))

@app.route('/progress/')
@login_required
def progress():
    user = Users.query.filter_by(username=current_user.username).first()
    
    return render_template('progress.html', titles = titles, title = "Progress", titles_keys = list(titles.keys()), progress_data = genProgressData(Users.query.filter_by(username=current_user.username).first()), completion_data = genChapterCompletion(Users.query.filter_by(username=current_user.username).first()), excludeTitle = False, courseComplete = courseCompleted(user))

# logout
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("index"))

# Redirect to index when accessing part of site without proper unauthorization
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('index'))

# Certificate download URL
@app.route('/certification')
@login_required
def certification():
    user = Users.query.filter_by(username=current_user.username).first()
    if courseCompleted(user):
        # generate a certification using user data
        tpl = genCert(f"{user.fname} {user.lname}", user.cdate)
        tpl.save(f"{os.getcwd()}/userdata/certs/{user.username}_cert.docx")

        # send through browser download
        return send_file(f"{os.getcwd()}/userdata/certs/{user.username}_cert.docx", as_attachment=True)


    return render_template('home.html', titles = titles, title = "Home", titles_keys = list(titles.keys()), progress_data = genProgressData(Users.query.filter_by(username=current_user.username).first()), completion_data = genChapterCompletion(Users.query.filter_by(username=current_user.username).first()), excludeTitle = False, courseComplete = courseCompleted(user))

if __name__ == "__main__":
    app.run()