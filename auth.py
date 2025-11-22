"""
Authentication module
"""

import bcrypt
from database import Database


class Auth:
    def __init__(self):
        self.db = Database()

    def hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password, password_hash):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def create_user(self, email, password, name):
        """Create new user with hashed password"""
        password_hash = self.hash_password(password)
        return self.db.create_user(email, password_hash, name)

    def authenticate(self, email, password):
        """Authenticate user"""
        user = self.db.get_user_by_email(email)

        if user and self.verify_password(password, user.password_hash):
            return user

        return None
