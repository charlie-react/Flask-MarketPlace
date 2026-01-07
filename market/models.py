from market import db,bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer, default=1000)
    items = db.relationship('Item', backref='owned_by', lazy=True)

    @property
    def pretty_budget(self):
        return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute') #raised a read-only exception deliberately
    @password.setter
    def password(self, password_plaintext):
        self.password_hash =bcrypt.generate_password_hash(password_plaintext).decode('utf-8')

    def verify_password(self,password_plaintext):
        return bcrypt.check_password_hash(self.password_hash,password_plaintext)

class Item(db.Model):
    name = db.Column(db.String(length=20),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    barcode = db.Column(db.String(length=12),unique=True,nullable=False)
    description = db.Column(db.String(length=1024),nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    owner=db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Item {self.name}, {self.owner}"