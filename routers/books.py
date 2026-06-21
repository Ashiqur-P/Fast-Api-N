from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import BookModel
from schemas import BookResponse, BookCreateUpdate

# রাউটার ইনিশিয়ালাইজেশন
router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
def get_all_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    stmt = select(BookModel)
    if search:
        stmt = stmt.where(BookModel.name.ilike(f"%{search}%"))
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    stmt = select(BookModel).where(BookModel.id == book_id)
    book = db.execute(stmt).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreateUpdate, db: Session = Depends(get_db)):
    new_book = BookModel(**book_in.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def update_book(book_id: int, book_in: BookCreateUpdate, db: Session = Depends(get_db)):
    stmt = select(BookModel).where(BookModel.id == book_id)
    book = db.execute(stmt).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
    
    update_data = book_in.model_dump()
    for key, value in update_data.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    stmt = select(BookModel).where(BookModel.id == book_id)
    book = db.execute(stmt).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
    
    db.delete(book)
    db.commit()
    return {"message": f"Book with id {book_id} has been deleted successfully"}