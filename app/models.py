from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

'''class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64), unique=False, index=True)
    population = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '{} {}'.format(self.city, self.population)
        '''


# authenticated user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.Integer(64))
    disciplinary_status = db.Column(db.String(64))
    user_type = db.Column(db.String(64))
    password_hash = db.Column(db.String(256), unique=True)
    def set_password(self, password):
        # Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))
