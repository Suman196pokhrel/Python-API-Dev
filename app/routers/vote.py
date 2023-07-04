from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserLogin
from .. import models
from ..utils.helpers import verify_hash
from ..oauth2 import create_access_token, verify_access_token, get_current_user
from ..schemas import Vote


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)



@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {vote.post_id} does not exist")
     



    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id , models.Votes.user_id== current_user.id)
    foundVote = vote_query.first()


    if(vote.dir ==1):

        if(foundVote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added Vote"}

    else:

        if not foundVote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote Does not Exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Successfully deleted Vote"}

