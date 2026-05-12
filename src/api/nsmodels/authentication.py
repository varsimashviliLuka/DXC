from flask_restx import reqparse, inputs
from src.extensions import api


auth_ns = api.namespace('Authentification', description='API მომხმარებლის აუტენტიფიკაციის შესახებ', path='/api/auth')

registration_parser = reqparse.RequestParser()

registration_parser.add_argument('email', type=inputs.email(check=True), required=True, help="გთხოვთ შეიყვანეთ მეილი luka.varsimashvili@iliauni.edu.ge")
registration_parser.add_argument('password', type=str, required=True, help="გთხოვთ შეიყვანეთ პაროლი")
registration_parser.add_argument('passwordRepeat', type=str, required=True, help='გთხოვთ გაიმეორეთ პაროლი')
registration_parser.add_argument('phone_number', type=str, required=True, help='გთხოვთ შეიყვანეთ ტელეფონის ნომერი')
registration_parser.add_argument('personal_number', type=str, required=True, help='გთხოვთ შეიყვანეთ პირადი ნომერი')


# Auth parser
auth_parser = reqparse.RequestParser()
auth_parser.add_argument("email_or_phone_number", required=True, type=str, help="გთხოვთ შეიყვანეთ მეილი luka.varsimashvili@iliauni.edu.ge ან ტელეფონის ნომერი 555123456")
auth_parser.add_argument("password", required=True, type=str, help="გთხოვთ შეიყვანეთ პაროლი")