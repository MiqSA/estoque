from model.User import User
from datetime import datetime, timedelta
import hashlib, base64, json, jwt
from config import app_config, app_active
config = app_config[app_active]


class UserController():
    def __init__(self):
        self.user_model = User()

    def login(self, email, password):
        """Pega os dados de e-mail e salva no atributo da model de usuário. """
        self.user_model.email = email
        """ Verifica se o usuário existe no banco de dados """
        result = self.user_model.get_user_by_email()
        """ Caso o usuário exista o result não será None """
        if result is not None:
            """ Verifica se o password que o usuário enviou, agora convertido em hash, é 
            igual ao password que foi pego no banco de dados para esse usuário."""
            res = self.user_model.verify_password(password, result.password)
            # Se for o mesmo retornará True
            if res:
                return result
            else:
                return {}
        return {}

    def get_admin_login(self, user_id):
        self.user_model.id = user_id
        response = self.user_model.get_user_by_id()
        return response

    def recovery(email):
        return ''

    def get_user_by_id(self, user_id):
        result = {}
        try:
            self.user_model.id = user_id
            res = self.user_model.get_user_by_id()
            result = {
                'id': res.id,
                'name': res.username,
                'email': res.email,
                'date_created': res.date_created
            }
            status = 200
        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }

    def verify_auth_token(self, access_token):
        status = 401
        try:
            jwt.decode(access_token, config.SECRET, algorithm='HS256')
            message = 'Token válido'
            status = 200
        except jwt.ExpiredSignatureError:
            message = 'Token expirado, realize um novo login'
        except:
            message = 'Token inválido'
        return {
            'message': message,
            'status': status
        }

    def generate_auth_token(self, data, exp=30, time_exp=False):
        if time_exp == True:
            date_time = data['exp']
        else:
            date_time = datetime.utcnow() + timedelta(minutes=exp)
        dict_jwt = {
            'id': data['id'],
            'username': data['username'],
            "exp": date_time
        }
        access_token = jwt.encode(dict_jwt, config.SECRET, algorithm = 'HS256')
        return access_token

