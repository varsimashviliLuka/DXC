from flask_restx import Resource

from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import User, BalanceTransaction
from src.api.nsmodels import user_ns, user_parser, update_user_parser, balance_parser


@user_ns.route('/user')
@user_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class UserApi(Resource):
    @jwt_required()
    @user_ns.doc(parser=user_parser)
    @user_ns.doc(security='JsonWebToken')
    def post(self):
        '''კონკრეტული მომხმარებლის შესახებ ინფორმაციის მიღება'''

        args = user_parser.parse_args()
        identity = get_jwt_identity()
        current_user = User.query.filter_by(uuid=identity).first()
        if not current_user:
            return {"error": "თქვენ არ გაქვთ წვდომა ამ მონაცემებთან."}, 403
        if current_user.role != 'admin':
            return {"error": "თქვენ არ გაქვთ წვდომა ამ მონაცემებთან."}, 403
        user = User.query.filter_by(id=args["id"]).first()
        if not user:
            return {"error": "მომხმარებელი ვერ მოიძებნა."}, 404
        
        return {'user': user.generateJson()}, 200
    
    @jwt_required()
    @user_ns.doc(security='JsonWebToken')
    def get(self):
        '''ყველა მომხმარებლის შესახებ ინფორმაციის მიღება'''

        identity = get_jwt_identity()
        current_user = User.query.filter_by(uuid=identity).first()
        if not current_user:
            return {"error": "თქვენ არ გაქვთ წვდომა ამ მონაცემებთან."}, 403
        if current_user.role != 'admin':
            return {"error": "თქვენ არ გაქვთ წვდომა ამ მონაცემებთან."}, 403
        users = User.query.all()
        users_data = [user.generateJson() for user in users]
        return {'users': users_data}, 200
    
    @jwt_required()
    @user_ns.doc(security='JsonWebToken')
    @user_ns.doc(parser=update_user_parser)
    def put(self):
        '''მომხმარებლის რედაქტირება'''

        identity = get_jwt_identity()
        current_user = User.query.filter_by(uuid=identity).first()

        if not current_user:
            return {"error": "თქვენ არ გაქვთ წვდომა ამ ფუნქციებთან."}, 403

        if current_user.role != 'admin':
            return {"error": "თქვენ არ გაქვთ წვდომა ამ ფუნქციებთან."}, 403

        args = update_user_parser.parse_args()

        user = User.query.filter_by(id=args["id"]).first()

        if not user:
            return {"error": "მომხმარებელი ვერ მოიძებნა."}, 404

        # EMAIL VALIDATION
        if args["email"]:

            existing_email = User.query.filter_by(email=args["email"]).first()

            if existing_email and existing_email.id != user.id:
                return {
                    "error": "ელ.ფოსტის მისამართი უკვე რეგისტრირებულია."
                }, 400

            user.email = args["email"]

        # PHONE VALIDATION
        if args["phone_number"]:

            if len(args["phone_number"]) != 9 or not args["phone_number"].isdigit():
                return {
                    "error": "ტელეფონის ნომერი უნდა შედგებოდეს 9 ციფრისგან."
                }, 400

            existing_phone = User.query.filter_by(
                phone_number=args["phone_number"]
            ).first()

            if existing_phone and existing_phone.id != user.id:
                return {
                    "error": "ტელეფონის ნომერი უკვე რეგისტრირებულია."
                }, 400

            user.phone_number = args["phone_number"]

        # PERSONAL NUMBER VALIDATION
        if args["personal_number"]:

            if len(args["personal_number"]) != 11 or not args["personal_number"].isdigit():
                return {
                    "error": "პირადი ნომერი უნდა შედგებოდეს 11 ციფრისგან."
                }, 400

            existing_personal_number = User.query.filter_by(
                personal_number=args["personal_number"]
            ).first()

            if existing_personal_number and existing_personal_number.id != user.id:
                return {
                    "error": "პირადი ნომერი უკვე რეგისტრირებულია."
                }, 400

            user.personal_number = args["personal_number"]
        if args["active"] is not None:
            user.active = args["active"]

        user.save()

        return {'user': user.generateJson()}, 200
    
    @jwt_required()
    @user_ns.doc(security='JsonWebToken')
    @user_ns.doc(parser=balance_parser)
    def patch(self):
        '''მომხმარებლის ბალანსის რედაქტირება'''

        args = balance_parser.parse_args()
        
        identity = get_jwt_identity()
        current_user = User.query.filter_by(uuid=identity).first()
        if not current_user:
            return {"error": "თქვენ არ გაქვთ წვდომა ამ ფუნქციებთან."}, 403
        if current_user.role != 'admin':
            return {"error": "თქვენ არ გაქვთ წვდომა ამ ფუნქციებთან."}, 403

        user = User.query.filter_by(id=args["id"]).first()
        if not user:
            return {"error": "მომხმარებელი ვერ მოიძებნა."}, 404
        if args["operator"] == "+":
            user.balance += args["amount"]
        if args["operator"] == "-":
            user.balance -= args["amount"]
        balance_transaction = BalanceTransaction(
            user_id=user.id,
            operator=args["operator"],
            amount=args["amount"]
        )
        balance_transaction.create()
        user.save()
        return {'user': user.generateJson()}, 200
    
        

@user_ns.route('/user/myuser')
@user_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class MyUserApi(Resource):
    @jwt_required()
    @user_ns.doc(security='JsonWebToken')
    def get(self):
        '''ავტორიზებული მომხმარებლის შესახებ ინფორმაციის მიღება'''

        identity = get_jwt_identity()
        current_user = User.query.filter_by(uuid=identity).first()
        if not current_user:
            return {"error": "მომხმარებელი ვერ მოიძებნა."}, 404
        data = {'email': current_user.email, 
                'phone_number': current_user.phone_number, 
                'personal_number': current_user.personal_number, 
                'identification_number': current_user.identification_number,
                'balance': current_user.balance,
                'active': current_user.active}
        return {'user': data}, 200