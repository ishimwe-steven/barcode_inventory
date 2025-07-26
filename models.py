from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    # Increase password_hash length, use 255 or more
    password_hash = db.Column(db.String(255), nullable=False)  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    telephone = db.Column(db.String(20))
    instagram = db.Column(db.String(255))
    email = db.Column(db.String(100))
    barcode_path = db.Column(db.String(255))
