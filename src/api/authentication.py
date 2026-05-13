from flask import jsonify
from flask_restx import Resource

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from src.models import User
from src.api.nsmodels import auth_ns, registration_parser, auth_parser

import random



@auth_ns.route('/registration')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RegistrationApi(Resource):
    @auth_ns.doc(parser=registration_parser)
    @auth_ns.doc(security='JsonWebToken')
    def post(self):
        '''მომხმარებლის რეგისტრაცია'''

        args = registration_parser.parse_args()
    
        # Validate password length and pattern
        if args["password"] != args["passwordRepeat"]:
            return {"error": "პაროლები არ ემთხვევა."}, 400
        
        if len(args["password"]) < 8:
            return {"error": "პაროლი უნდა იყოს მინიმუმ 8 სიმბოლო."}, 400

        if User.query.filter_by(email=args["email"]).first():
            return {"error": "ელ.ფოსტის მისამართი უკვე რეგისტრირებულია."}, 400
        
        if User.query.filter_by(personal_number=args["personal_number"]).first():
            return {"error": "პირადი ნომერი უკვე რეგისტრირებულია."}, 400
        
        if len(args["personal_number"]) != 11 or not args["personal_number"].isdigit():
            return {"error": "პირადი ნომერი უნდა შედგებოდეს 11 ციფრისგან."}, 400
        
        if User.query.filter_by(phone_number=args["phone_number"]).first():
            return {"error": "ტელეფონის ნომერი უკვე რეგისტრირებულია."}, 400
        
        if len(args["phone_number"]) != 9 or not args["phone_number"].isdigit():
            return {"error": "ტელეფონის ნომერი უნდა შედგებოდეს 9 ციფრისგან."}, 400
        while True:
            identification_number = random.randint(100000, 999999)
            if not User.query.filter_by(identification_number=identification_number).first():
                break

        new_user = User(
            email=args["email"],
            password=args["password"],
            phone_number=args["phone_number"],
            personal_number=args["personal_number"],
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
                "message": "წარმატებით გაიარეთ ავტორიზაცია.",
                "access_token": access_token})
            
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=False,      # True in production (HTTPS)
                samesite="Strict",
                path="/api/auth/refresh",
                max_age=30 * 24 * 60 * 60)

            return response
        
        # If the password is incorrect
        else:
            return {"error": "შეყვანილი პაროლი ან ელ.ფოსტა არასწორია."}, 400
        

@auth_ns.route('/refresh')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class AccessTokenRefreshApi(Resource):
    @jwt_required(refresh=True, locations=["cookies"])
    @auth_ns.doc(security='JsonWebToken')
    def post(self):
        '''JWT ტოკენის დარეფრეშება'''
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        response = jsonify({
            "access_token": access_token
        })

        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=False,
            samesite="Strict",
            path="/api/auth/refresh",
            max_age=30 * 24 * 60 * 60
        )

        return response
    
@auth_ns.route('/check')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class CheckAuthApi(Resource):
    @jwt_required()
    def get(self):
        return {"message": "მომხმარებელი ავტორიზებულია."}, 200

@auth_ns.route('/logout')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class LogoutApi(Resource):

    def post(self):

        response = jsonify({
            "message": "Logged out"
        })

        response.delete_cookie(
            "refresh_token",
            path="/api/auth/refresh"
        )

        return response    
