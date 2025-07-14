from flask import Flask
from auth import auth_blueprint
from models import db, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
# MySQL config example (update with your credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
