from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select

from ..database import get_session
from ..models import Posts, Votes
from ..oauth2 import get_current_user
from ..schemas import PostBase, PostCreate, PostsWithVotes

# Router dedicado a todo el CRUD de posts más el agregado de votos.
router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostsWithVotes])
def get_posts(db: Session = Depends(get_session),
              limit: int = 10,
              skip: int = 0,
              search: str = ""):
    """Lista los posts aplicando paginación, filtro por título y conteo de votos."""
    posts = db.exec(
        select(Posts, func.count(Votes.user_id).label("votes"))
        .join(Votes, Votes.post_id == Posts.id, isouter=True)
        .where(Posts.title.contains(search))
        .limit(limit)
        .offset(skip)
        .group_by(Posts.id)
        .order_by((func.count(Votes.user_id)).desc())
    ).all()
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostsWithVotes)
def get_a_post(id: int,
               db: Session = Depends(get_session),
               current_user: str = Depends(get_current_user)):
    """Devuelve un post específico, verificando que pertenezca al usuario autenticado."""
    post = db.exec(
        select(Posts, func.count(Votes.user_id).label("votes"))
        .join(Votes, Votes.post_id == Posts.id, isouter=True)
        .group_by(Posts.id)
        .where(Posts.id == id)
    ).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    if post.Posts.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    print(post)
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostCreate)
def create_post(payload: PostBase,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):
    """Crea un nuevo post asociándolo automáticamente al usuario autenticado."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    new_post = Posts(**payload.model_dump(), user_id=int(current_user))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostBase)
def update_post(id: int,
                payload: PostBase,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):
    """Permite editar un post siempre que sea propiedad del usuario autenticado."""
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    if post.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    # Actualizamos los campos manualmente para mantener el control sobre cada atributo.
    post.title = payload.title
    post.content = payload.content
    post.published = payload.published

    db.add(post)      # opcional, pero recomendable para dejar constancia del merge.
    db.commit()
    db.refresh(post)  # refrescamos para devolver la versión persistida.
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):
    """Elimina un post existente si pertenece al usuario autenticado."""
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    if post.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return
