from flask import Flask
import pickle
import joblib
from flask_sqlalchemy import SQLAlchemy


# instantiate SQLAlchemy to handle db process
db = SQLAlchemy()

#create the Flask app
app = Flask(__name__)

# load configuration from config.cfg
app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ai_model_file = "./application/static/model_weights/full_model_xgb.pkl"
extractor_file = "./application/static/model_weights/extractor.pkl"

app.debug = False

# Load AI model
with open(ai_model_file, 'rb') as f:
	ai_model = joblib.load(f)

# Load extractor instance
with open(extractor_file, 'rb') as f:
	extractor = joblib.load(f)

with app.app_context():
	db.init_app(app)
	from .models import User, Entry, Result
	db.create_all()
	db.session.commit()
	print('Created database!')

#run the file routes.py
from application import routes