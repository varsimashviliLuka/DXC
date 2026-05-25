from flask import jsonify
from flask_restx import Resource

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from src.models import User
from src.api.nsmodels import auth_ns, registration_parser, auth_parser

import random



@auth_ns.route('/registration')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RegistrationApi(Resource):
    @auth_ns.doc(parser=registration_parser)
    def post(self):
        '''მომხმარებლის რეგისტრაცია'''

        args = registration_parser.parse_args()
        normalized_personal_number = ''.join(ch for ch in args["personal_number"] if ch.isdigit())
        normalized_phone_number = ''.join(ch for ch in args["phone_number"] if ch.isdigit())

        if len(normalized_phone_number) == 12 and normalized_phone_number.startswith("995"):
            normalized_phone_number = normalized_phone_number[3:]
    
        # Validate password length and pattern
        if args["password"] != args["passwordRepeat"]:
            return {"error": "პაროლები არ ემთხვევა."}, 400
        
        if len(args["password"]) < 8:
            return {"error": "პაროლი უნდა იყოს მინიმუმ 8 სიმბოლო."}, 400

        if User.query.filter_by(email=args["email"]).first():
            return {"error": "ელ.ფოსტის მისამართი უკვე რეგისტრირებულია."}, 400
        
        if User.query.filter_by(personal_number=normalized_personal_number).first():
            return {"error": "პირადი ნომერი უკვე რეგისტრირებულია."}, 400
        
        if len(normalized_personal_number) != 11:
            return {"error": "პირადი ნომერი უნდა შედგებოდეს 11 ციფრისგან."}, 400
        
        if User.query.filter_by(phone_number=normalized_phone_number).first():
            return {"error": "ტელეფონის ნომერი უკვე რეგისტრირებულია."}, 400
        
        if len(normalized_phone_number) != 9:
            return {"error": "ტელეფონის ნომერი უნდა შედგებოდეს 9 ციფრისგან."}, 400
        while True:
            identification_number = str(random.randint(100000, 999999))
            if not User.query.filter_by(identification_number=identification_number).first():
                break

        new_user = User(
            email=args["email"],
            password=args["password"],
            phone_number=normalized_phone_number,
            personal_number=normalized_personal_number,
            identification_number=identification_number
        )

        new_user.create()
        return {"message": 'მომხმარებელი წარმატებით დარეგისტრირდა'}, 200
    
@auth_ns.route('/login')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class AuthorizationApi(Resource):
    @auth_ns.doc(parser=auth_parser)
    def post(self):
        '''მომხმარებლის სისტემაში შესვლა'''
        args = auth_parser.parse_args()

        # Look up the user by email or phone number
        user = User.query.filter(
            (User.email == args["email_or_phone_number"]) |
            (User.phone_number == args["email_or_phone_number"])
        ).first()
        if not user:
            return {"error": "შეყვანილი პაროლი ან ელ.ფოსტა არასწორია."}, 400

        # Check if the password matches
        if user.check_password(args["password"]):
            # Create tokens with the user's UUID as the identity
            access_token = create_access_token(identity=user.uuid)
            refresh_token = create_refresh_token(identity=user.uuid)

            response = jsonify({
                "message": "წარმატებით გაიარეთ ავტორიზაცია."})
            
            set_refresh_cookies(response, refresh_token)
            set_access_cookies(response, access_token)

            return response
        
        # If the password is incorrect
        else:
            return {"error": "შეყვანილი პაროლი ან ელ.ფოსტა არასწორია."}, 400
        

@auth_ns.route('/refresh')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class AccessTokenRefreshApi(Resource):
    @jwt_required(refresh=True)
    @auth_ns.doc(security='CsrfRefresh')
    def post(self):
        '''JWT ტოკენის დარეფრეშება'''
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        response = jsonify({
            "message": "წარმატებით დარეფრეშულია ავტორიზაციის ტოკენი."
        })

        set_refresh_cookies(response, refresh_token)
        set_access_cookies(response, access_token)

        return response


@auth_ns.route('/logout')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class LogoutApi(Resource):

    @jwt_required()
    @auth_ns.doc(security='CsrfAccess')
    def post(self):

        response = jsonify({
            "message": "Logged out"
        })

        unset_jwt_cookies(response)

        return response
    
