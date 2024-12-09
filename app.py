# CHECK THIS OUT FOR A CUSTOM ARTICLE ROUTING FUNCTION https://www.geeksforgeeks.org/flask-app-routing/
# IMPLEMENT WEBMANIFEST AND .ENV

from flask import *
from flask_sqlalchemy import *
from flask_login import *
from flask_wtf import *

app = Flask(__name__)
 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

app.config["SECRET_KEY"] = "XFYXGK3tQD52O5pgzeCfj4c7gWiFFAmZ"
# init
db = SQLAlchemy()

# enable csrf protection
csrf = CSRFProtect(app)

# login manager handles
login_manager = LoginManager()
login_manager.init_app(app)

# Create user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)

    fname = db.Column(db.String(250),
                         nullable=False)
    lname = db.Column(db.String(250),
                         nullable=False)
    
    cdate = db.Column(db.String(250),
                         default="none")

# init rest of appp
db.init_app(app)
 
with app.app_context():
    db.create_all()
# testing flask functionality
with app.test_request_context('/abc/efg'):
    print(request.path)

# func to load in user
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

# import routes
import routes.login
import routes.articles

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home/')
# login required integrates blocked part of page with login_manager
@login_required
def home():
    user = Users.query.filter_by(username=current_user.username).first()
    
    return render_template('home.html')

@app.route('/progress/')
@login_required
def progress():
    user = Users.query.filter_by(username=current_user.username).first()
    
    return render_template('progress.html')

# logout
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("index"))

# redirect to index when accessing unauthorized part of site
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)