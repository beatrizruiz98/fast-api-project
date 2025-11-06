from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlmodel import Session, select
from ..schemas import PostIn, PostBase
from ..database import get_session
from ..models import Posts

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostIn])
def get_posts(db: Session = Depends(get_session)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.exec(select(Posts)).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostIn)
def create_post(payload: PostIn, db: Session = Depends(get_session)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = Posts(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostIn)
def get_a_post(id: int, db: Session = Depends(get_session)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_session)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted = cursor.fetchone()
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    db.delete(post)
    db.commit()
    # conn.commit()
    return

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostBase)
def update_post(id: int, payload: PostIn, db: Session = Depends(get_session)):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, post.published, id),
    # )
    # updated = cursor.fetchone()
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    # actualizamos los campos manualmente
    post.title = payload.title
    post.content = payload.content
    post.published = payload.published

    db.add(post)      # opcional, pero recomendable
    db.commit()
    db.refresh(post)  # para devolver el valor actualizado
    # conn.commit()
    return post