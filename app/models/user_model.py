import bcrypt
import jwt
import os
import secrets
from datetime import datetime, timedelta
from bson import ObjectId
from database import users_collection

class User:
    def __init__(self, username, email, password, role="user"):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.is_email_verified = False
        self.refresh_token = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def hash_password(self):
        """Hash the user's password before saving."""
        self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Check if the entered password matches the stored hash."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def generate_access_token(self):
        """Generate JWT access token"""
        payload = {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "role": self.role,
            "exp": datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRY", "30")))
        }
        return jwt.encode(payload, os.getenv("ACCESS_TOKEN_SECRET"), algorithm="HS256")

    def generate_refresh_token(self):
        """Generate JWT refresh token"""
        payload = {
            "id": str(self.id),
            "exp": datetime.utcnow() + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRY", "7")))
        }
        return jwt.encode(payload, os.getenv("REFRESH_TOKEN_SECRET"), algorithm="HS256")

    def save(self):
        """Save user to MongoDB"""
        self.hash_password()
        user_dict = self.__dict__
        result = users_collection.insert_one(user_dict)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        user = users_collection.find_one({"email": email})
        if user:
            return User(**user)
        return None
