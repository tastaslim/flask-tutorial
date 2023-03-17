from config import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(800), nullable=False)


class UserRegistrationModel(UserModel):
    email = db.Column(db.String, unique=True, nullable=False)
