
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
import uuid
import time
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session 
from ..schemas import PostCreate, Post, PostOut
from .. import oauth2
from sqlalchemy import func





router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)




@router.get("/",response_model=List[PostOut])
def get_posts(db:Session= Depends(get_db), curr_user:int = Depends(oauth2.get_current_user),limit:int=10, search: Optional[str]=""):
    

    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).all()
    
    results =  db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Posts.id, isouter=True).group_by(models.Posts.id).all()
    # print(results)
    
    return results


@router.get("/{id}", response_model=PostOut)
def get_post(id:int,db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    # post = db.query(models.Posts).filter(models.Posts.id == id).first()

    post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post with id {id} not found")

        
    else:
        return post


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate,db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    
    post = post.dict()
    new_post = models.Posts(**post, user_id = curr_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@router.delete("/{id}")
def delete_post(id:int,db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The requested post with id {id} does not exists" )

    else:
        if post_query.first().user_id != curr_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorized to perform requested action" )
            

        else:

            post_query.delete(synchronize_session=False)
            db.commit()
            return {
                "message":"Post deleted Sucessfully",
            }


@router.put("/{id}", response_model=Post)
def update_post(id:int, post:PostCreate,db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The requested post with id {id} does not exists" )

    else:
        if post_query.first().user_id != curr_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorized to perform requested action" )
            

        else:

            
            updated_post = post.dict()
            post_query.update(updated_post, synchronize_session=False)
            db.commit()
            
            return post_query.first()

