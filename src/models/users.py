import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.models.base import BaseModel


class User(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.String(255), unique=True, default=lambda: str(uuid.uuid4()))

    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)

    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    personal_number = db.Column(db.String(20), unique=True, nullable=False)

    identification_number = db.Column(db.String(10), unique=True, nullable=False)

    role = db.Column(db.String(20), nullable=False, default="user")

    balance = db.Column(db.Float, nullable=False, default=0.0)

    active = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generateJson(self):
        result = {'email': self.email,
                  'id': self.id,
                  'uuid': self.uuid,
                  'phone_number': self.phone_number,
                  'personal_number': self.personal_number,
                  'identification_number': self.identification_number,
                  'role': self.role,
                  'balance': self.balance,
                  'active': self.active}
        return result


    def __repr__(self):
        return f'{self.generateJson()}'