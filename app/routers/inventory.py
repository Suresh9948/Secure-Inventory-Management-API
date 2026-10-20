from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import authenticated, manager_or_admin, admin_only
from app.models.inventory import Category, Product, Supplier
from app.schemas.inventory import CategoryCreate, CategoryUpdate, CategoryOut, ProductCreate, ProductUpdate, ProductOut, SupplierCreate, SupplierUpdate, SupplierOut
from app.services.inventory import InventoryService

router = APIRouter(tags=["Inventory"], dependencies=[Depends(authenticated)])

def crud_router(prefix, model, create_schema, update_schema, out_schema, write_dependency, allow_delete):
    r = APIRouter(prefix=prefix)
    @r.post("", response_model=out_schema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(write_dependency)])
    def create(data: create_schema, db: Session = Depends(get_db)):
        return InventoryService(db).create(model, data.model_dump())
    @r.get("", response_model=list[out_schema])
    def list_items(db: Session = Depends(get_db)):
        return InventoryService(db).list(model)
    @r.get("/{item_id}", response_model=out_schema)
    def get_item(item_id: int, db: Session = Depends(get_db)):
        return InventoryService(db).get(model, item_id)
    @r.put("/{item_id}", response_model=out_schema, dependencies=[Depends(write_dependency)])
    def update(item_id: int, data: update_schema, db: Session = Depends(get_db)):
        return InventoryService(db).update(model, item_id, data.model_dump(exclude_unset=True))
    if allow_delete:
        @r.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_only)])
        def delete(item_id: int, db: Session = Depends(get_db)):
            InventoryService(db).delete(model, item_id)
            return None
    return r

router.include_router(crud_router("/categories", Category, CategoryCreate, CategoryUpdate, CategoryOut, admin_only, True))
router.include_router(crud_router("/products", Product, ProductCreate, ProductUpdate, ProductOut, manager_or_admin, True))
router.include_router(crud_router("/suppliers", Supplier, SupplierCreate, SupplierUpdate, SupplierOut, admin_only, True))
