# app/core/security.py
from datetime import datetime, timedelta
import hashlib
import string
import random
import re
import secrets
import time
from typing import Dict, Any, Optional
import jwt
from passlib.context import CryptContext
import hmac

from app.core.settings import Settings

class SecurityUtils:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=12  # Stronger hashing with more rounds
        )
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash using constant-time comparison"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(self, password: str) -> str:
        """Hash a password for storage"""
        return self.pwd_context.hash(password)
    
    def is_password_strong(self, password: str) -> bool:
        """Check if a password meets security requirements"""
        if len(password) < 8:  # Using a default value if settings.password_min_length is not available
            return False
        
        # Check for complexity requirements
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        return has_uppercase and has_lowercase and has_digit and has_special
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create a simple token using SHA256 with random key"""
        # Get username
        username = data.get("username", "")
        
        # Get current timestamp
        timestamp = str(int(time.time()))
        
        # Generate random component
        random_key = secrets.token_hex(16)  # 16 bytes of randomness
        
        # Concatenate all components
        raw_token = f"{timestamp}:{username}:{random_key}"
        
        # Create SHA256 hash
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        
        # Return token
        return hashed_token
        
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token and return the payload if valid"""
        try:
            # Decode and verify token
            payload = jwt.decode(
                token, 
                "secret_key",  # Default value if settings.secret_key is not available
                algorithms=["HS256"],  # Default value if settings.token_algorithm is not available
                options={
                    "verify_signature": True, 
                    "verify_exp": True, 
                    "verify_iat": True,
                }
            )
            return payload
        except jwt.PyJWTError:
            return None
    
    def generate_recovery_code(self) -> str:
        """Generate a secure recovery code for password reset"""
        # Use both letters and numbers for better usability
        chars = string.ascii_letters + string.digits
        # 10 character code is reasonably secure but usable
        return ''.join(secrets.choice(chars) for _ in range(10))
    
    def secure_compare(self, a: str, b: str) -> bool:
        """Perform a constant-time comparison of two strings to prevent timing attacks"""
        if a is None or b is None:
            return False
        return hmac.compare_digest(a, b)