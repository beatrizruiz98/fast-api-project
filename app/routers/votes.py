from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Posts, Votes
from ..oauth2 import get_current_user
from ..schemas import Vote

# Router con la lógica para crear o eliminar votos sobre posts.
router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)


@router.post("/")
def vote(payload: Vote,
         db: Session = Depends(get_session),
         current_user: str = Depends(get_current_user)):
    """Crea un voto (dir=1) o lo elimina (dir=0) según la dirección solicitada."""
    new_vote = Votes(**payload.model_dump(), user_id=int(current_user))
    vote_query = db.exec(select(Votes).where(
        Votes.post_id == new_vote.post_id,
        Votes.user_id == new_vote.user_id
    )).first()

    post_id_list = db.exec(select(Posts.id)).all()
    if new_vote.post_id not in post_id_list:
        # Si se intenta votar un post que no existe, lanzamos error
        raise HTTPException(status_code=404, detail=f"Post {new_vote.post_id} does not exist")

    if payload.dir == 1:
        if vote_query:
            # Si el voto ya existe y se intenta crear otro, lanzamos error
            raise HTTPException(status_code=409, detail=f"User {new_vote.user_id} already voted for post {new_vote.post_id}")
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        raise HTTPException(status.HTTP_201_CREATED, detail="Vote added successfully")
    if payload.dir == 0:
        if not vote_query:
            raise HTTPException(status_code=400, detail=f"User did not vote the post {new_vote.post_id}")
        db.delete(vote_query)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Vote removed successfully")
