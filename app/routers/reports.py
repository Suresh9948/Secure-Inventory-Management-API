from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_roles
from app.models.user import UserRole
from app.models.inventory import Product

router = APIRouter(prefix="/reports", tags=["Reports"], dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))])

@router.get("/inventory")
def inventory_report(db: Session = Depends(get_db)):
    products = list(db.scalars(select(Product).order_by(Product.name)))
    return {"product_count": len(products), "total_units": sum(p.quantity for p in products),
            "products": [{"id": p.id, "name": p.name, "quantity": p.quantity} for p in products]}

@router.get("/restocking")
def restocking_report(threshold: int = 10, db: Session = Depends(get_db)):
    if threshold < 0:
        raise HTTPException(status_code=422, detail="Threshold must be non-negative")
    products = list(db.scalars(select(Product).where(Product.quantity <= threshold).order_by(Product.quantity)))
    return {"threshold": threshold, "items": [{"id": p.id, "name": p.name, "quantity": p.quantity} for p in products]}
