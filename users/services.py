
from .models import User

class UserService:

    def __init__(self):
        pass

    @staticmethod
    def is_username_exists( username):
        return User.objects.filter(username=username).exists()
    
    @staticmethod
    def is_email_exists(email):
        return User.objects.filter(email=email).exists()
    
    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()
    
    @staticmethod
    def get_user_by_id(id):
        return User.objects.filter(id=id).first()