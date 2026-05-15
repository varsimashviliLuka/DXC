from src.extensions import db
from src.models.base import BaseModel

class BalanceTransaction(db.Model, BaseModel):
    __tablename__ = "balance_transactions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    operator = db.Column(db.String(1), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('balance_transactions', lazy=True))

    def generateJson(self):
        result = {'id': self.id,
                  'user_id': self.user_id,
                  'operator': self.operator,
                  'amount': self.amount,
                  'timestamp': f'{self.timestamp}'}
        return result

    def __repr__(self):
        return f'<BalanceTransaction {self.id} - User ID: {self.user_id}, Operator: {self.operator}, Amount: {self.amount}>'