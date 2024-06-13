from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
import models, schemas, utils
from database import SessionLocal, engine
from datetime import timedelta


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(utils.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)):
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Books Endpoints
@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(utils.get_db), current_user: schemas.UserBase = Depends(utils.get_current_user)):
    if current_user.role == "admin":
        books = db.query(models.Book).offset(skip).limit(limit).all()
    else:
        books = db.query(models.Book).filter(models.Book.owner_id == current_user.id).offset(skip).limit(limit).all()
    
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(utils.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(utils.get_db), current_user: schemas.UserBase = Depends(utils.get_current_user)):
    db_book = models.Book(**book.dict(), owner_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(utils.get_db), current_user: schemas.UserBase = Depends(utils.get_current_user)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if db_book.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions to update this book")
    
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(utils.get_db), current_user: schemas.UserBase = Depends(utils.get_current_admin_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete books")
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

# Authors Endpoints
@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(utils.get_db)):
    return db.query(models.Author).offset(skip).limit(limit).all()

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(utils.get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    print(db_author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(utils.get_db)):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(utils.get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.delete("/authors/{author_id}", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(utils.get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return db_author

# Genres Endpoints
@app.get("/genres/", response_model=List[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 10, db: Session = Depends(utils.get_db)):
    return db.query(models.Genre).offset(skip).limit(limit).all()

@app.get("/genres/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(utils.get_db)):
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

@app.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(utils.get_db)):
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@app.put("/genres/{genre_id}", response_model=schemas.Genre)
def update_genre(genre_id: int, genre: schemas.GenreUpdate, db: Session = Depends(utils.get_db)):
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    for key, value in genre.dict().items():
        setattr(db_genre, key, value)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@app.delete("/genres/{genre_id}", response_model=schemas.Genre)
def delete_genre(genre_id: int, db: Session = Depends(utils.get_db)):
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    db.delete(db_genre)
    db.commit()
    return db_genre
