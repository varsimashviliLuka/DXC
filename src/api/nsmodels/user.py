from flask_restx import reqparse, inputs
from src.extensions import api


user_ns = api.namespace('Users', description='API მომხმარებლის შესახებ', path='/api')

user_parser = reqparse.RequestParser()

user_parser.add_argument('id', type=str, required=True, help="გთხოვთ შეიყვანეთ მომხმარებლის ID")

update_user_parser = reqparse.RequestParser()

update_user_parser.add_argument('id', type=str, required=True, help="გთხოვთ შეიყვანეთ მომხმარებლის ID")
update_user_parser.add_argument('email', type=inputs.email(check=True), required=False, help="გთხოვთ შეიყვანეთ მეილი")
update_user_parser.add_argument('phone_number', type=str, required=False, help='გთხოვთ შეიყვანეთ ტელეფონის ნომერი')
update_user_parser.add_argument('personal_number', type=str, required=False, help='გთხოვთ შეიყვანეთ პირადი ნომერი')
update_user_parser.add_argument('active', type=inputs.boolean, required=False, help='გთხოვთ შეიყვანეთ მომხმარებლის აქტივობის სტატუსი (true/false)')

balance_parser = reqparse.RequestParser()

balance_parser.add_argument('id', type=str, required=True, help="გთხოვთ შეიყვანეთ მომხმარებლის ID")
balance_parser.add_argument('operator', type=str, required=True, choices=['+', '-'], help="გთხოვთ შეიყვანეთ ოპერატორი (+ ან -)")
balance_parser.add_argument('amount', type=float, required=True, help="გთხოვთ შეიყვანეთ თანხა")

