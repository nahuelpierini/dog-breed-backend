from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from typing import Optional

class User(UserMixin):
    """
    A class to represent a user in the application.

    This class extends Flask-Login's UserMixin to support session management for user authentication.
    """
    
    def __init__(self, userid: str, email: str, upassword: str, firstname: str = "", lastname: str = "", 
                 birthdate: Optional[str] = None, country: str = ""):
        self.userid = userid
        self.email = email
        self.upassword = upassword
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.country = country

    def get_id(self) -> str:
        return self.userid

    @classmethod
    def check_password(cls, hashed_password: str, password: str) -> bool:
        return check_password_hash(hashed_password, password)
    
    @classmethod
    def generate_password(cls, password: str) -> str:
        return generate_password_hash(password)
