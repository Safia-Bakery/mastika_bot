import re
import random
import string
from typing import Union,Any
from jose import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')   # should be kept secret
JWT_REFRESH_SECRET_KEY =  os.environ.get('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

def generate_random_username(full_name, phone_number, length=5):
    # Remove spaces and special characters from the full name
    full_name = re.sub(r'[^a-zA-Z0-9]', '', full_name)
    # Extract a portion of the phone number (e.g., the last four digits)
    phone_number = phone_number[-4:]
    # Generate a random string of a specified length
    random_part = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    # Combine the processed full name, extracted phone number, and random part
    username = full_name + phone_number + random_part
    return username



def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def phone_checker(phone_number):


    pattern = r'^9989[012345789][0-9]{7}$'
    if re.match(pattern, phone_number):
        return True
    else:
        return False