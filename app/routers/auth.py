from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserLogin
from .. import models
from ..utils.helpers import verify_hash
from ..oauth2 import create_access_token, verify_access_token
from ..schemas import Token


router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)


@router.post("/", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Credentials")
    
    else:
        if not verify_hash(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
        else:
            # create a token
            access_token = create_access_token(data = {"user_id":user.id})

            # return token
            return {
                "access_token":access_token,
                "token_type":"bearer"
            }



