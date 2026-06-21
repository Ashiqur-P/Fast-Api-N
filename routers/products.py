from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import ProductModel
from schemas import ProductResponse, ProductCreateUpdate

# রাউটার ইনিশিয়ালাইজেশন
router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    stmt = select(ProductModel)
    if search:
        stmt = stmt.where(ProductModel.title.ilike(f"%{search}%"))
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    stmt = select(ProductModel).where(ProductModel.id == product_id)
    product = db.execute(stmt).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreateUpdate, db: Session = Depends(get_db)):
    new_product = ProductModel(**product_in.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(product_id: int, product_in: ProductCreateUpdate, db: Session = Depends(get_db)):
    stmt = select(ProductModel).where(ProductModel.id == product_id)
    product = db.execute(stmt).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
    update_data = product_in.model_dump()
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    stmt = select(ProductModel).where(ProductModel.id == product_id)
    product = db.execute(stmt).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
    db.delete(product)
    db.commit()
    return {"message": f"Product with id {product_id} has been deleted successfully"}