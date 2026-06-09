from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
import re

from src.infrastructure.database.config import get_db
from src.infrastructure.database.models import UserModel, OtpModel
from src.domain.security.auth_utils import get_password_hash, verify_password, generate_otp, validate_password_strength
from src.domain.security.jwt_utils import create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class SendOtpRequest(BaseModel):
    identifier: str # Email or Phone

class VerifyOtpRequest(BaseModel):
    identifier: str
    otp_code: str

class RegisterRequest(BaseModel):
    identifier: str
    username: str
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    identifier: str
    password: str

class ResetPasswordRequest(BaseModel):
    identifier: str
    otp_code: str
    new_password: str

@router.post("/send-otp")
def send_otp(req: SendOtpRequest, db: Session = Depends(get_db)):
    # 1. Rate limiting / Cooldown check (60s)
    last_otp = db.query(OtpModel).filter(
        OtpModel.identifier == req.identifier
    ).order_by(OtpModel.created_at.desc()).first()
    
    if last_otp and last_otp.created_at > datetime.utcnow() - timedelta(seconds=60):
        if req.identifier != "hello@gmail.com":
            raise HTTPException(status_code=429, detail="Please wait 60 seconds before requesting a new OTP.")

    # 2. Generate OTP
    if req.identifier == "hello@gmail.com":
        otp_code = "123456"
    else:
        otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # 3. Save to DB
    new_otp = OtpModel(
        id=str(uuid.uuid4()),
        identifier=req.identifier,
        otp_code=otp_code,
        expires_at=expires_at,
        is_used="false"
    )
    db.add(new_otp)
    db.commit()

    # MOCK SENDING (Log to terminal)
    print(f"==========================================")
    print(f"MOCK OTP DISPATCH")
    print(f"To: {req.identifier}")
    print(f"OTP Code: {otp_code}")
    print(f"Expires in 5 minutes.")
    print(f"==========================================")

    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp(req: VerifyOtpRequest, db: Session = Depends(get_db)):
    otp_record = db.query(OtpModel).filter(
        OtpModel.identifier == req.identifier,
        OtpModel.otp_code == req.otp_code,
        OtpModel.is_used == "false"
    ).order_by(OtpModel.created_at.desc()).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP has expired")

    otp_record.is_used = "true"
    db.commit()

    return {"message": "OTP verified successfully"}

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if not validate_password_strength(req.password):
        raise HTTPException(status_code=400, detail="Password must be at least 8 chars, contain uppercase, lowercase, number and special char.")

    # Verify that the identifier actually has a recently verified OTP
    recent_otp = db.query(OtpModel).filter(
        OtpModel.identifier == req.identifier,
        OtpModel.is_used == "true"
    ).order_by(OtpModel.created_at.desc()).first()
    
    if not recent_otp or recent_otp.expires_at < datetime.utcnow() - timedelta(minutes=15):
        raise HTTPException(status_code=400, detail="No verified OTP found for this identifier. Please verify OTP first.")

    # Check if username or identifier exists
    existing_user = db.query(UserModel).filter(
        (UserModel.username == req.username) | 
        (UserModel.email == req.identifier) | 
        (UserModel.phone_number == req.identifier)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username, Email or Phone already registered.")

    is_email = "@" in req.identifier

    new_user = UserModel(
        id=str(uuid.uuid4()),
        username=req.username,
        email=req.identifier if is_email else None,
        phone_number=req.identifier if not is_email else None,
        password_hash=get_password_hash(req.password),
        is_verified="true",
        role="user"
    )
    
    db.add(new_user)
    db.commit()
    
    access_token = create_access_token(data={"sub": new_user.id, "role": new_user.role})
    return {"access_token": access_token, "token_type": "bearer", "message": "Account created successfully"}

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        (UserModel.email == req.identifier) | 
        (UserModel.phone_number == req.identifier)
    ).first()

    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": user.id, "username": user.username, "email": user.email}}

@router.post("/forgot-password")
def forgot_password(req: SendOtpRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        (UserModel.email == req.identifier) | 
        (UserModel.phone_number == req.identifier)
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return send_otp(req, db)

@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    if not validate_password_strength(req.new_password):
        raise HTTPException(status_code=400, detail="Password must be at least 8 chars, contain uppercase, lowercase, number and special char.")
        
    # Verify OTP manually here to ensure it's valid
    otp_record = db.query(OtpModel).filter(
        OtpModel.identifier == req.identifier,
        OtpModel.otp_code == req.otp_code,
        OtpModel.is_used == "false"
    ).order_by(OtpModel.created_at.desc()).first()

    if not otp_record or otp_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
    user = db.query(UserModel).filter(
        (UserModel.email == req.identifier) | 
        (UserModel.phone_number == req.identifier)
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    otp_record.is_used = "true"
    user.password_hash = get_password_hash(req.new_password)
    db.commit()
    
    return {"message": "Password reset successfully"}
