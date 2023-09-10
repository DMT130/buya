from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

# Create a FastAPI app
app = FastAPI()

# Some configurations
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simulated database (for demonstration)
db_users = {}
db_tokens = {}
verification_tokens = {}

# Pydantic models for user registration and login
class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    email: str = None

# Password hashing
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Password Bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to verify a user's password
def verify_password(plain_password, hashed_password):
    return password_hasher.verify(plain_password, hashed_password)

# Function to create a new user
def create_user(user: UserRegister):
    hashed_password = password_hasher.hash(user.password)
    db_users[user.email] = {"email": user.email, "password": hashed_password, "is_verified": False}
    return user

# Function to generate an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Route for user registration
@app.post("/register")
def register(user: UserRegister):
    if user.email in db_users:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(user)
    
    # Simulate sending a verification email
    verification_token = "unique_verification_token"  # Generate a unique token
    verification_tokens[verification_token] = user.email  # Associate token with email
    # Send email with the verification link containing the token
    
    return {"message": "Registration successful. Please check your email for verification instructions."}

# Route for verifying email using the verification token
@app.get("/verify-email/{token}")
def verify_email(token: str):
    if token in verification_tokens:
        user_email = verification_tokens.pop(token)
        db_users[user_email]["is_verified"] = True
        return {"message": "Email verification successful"}
    raise HTTPException(status_code=404, detail="Token not found")

# Route for user login
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_users.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]) or not user["is_verified"]:
        raise HTTPException(status_code=400, detail="Incorrect email or password or unverified email")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route that requires authentication using token
@app.get("/protected")
def protected_route(current_user: TokenData = Depends(oauth2_scheme)):
    return {"message": "You are accessing a protected route", "user_email": current_user.email}
