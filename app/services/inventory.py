from fastapi import HTTPException
from app.repositories.inventory import InventoryRepository
from app.models.inventory import Category, Product, Supplier

class InventoryService:
    def __init__(self, db):
        self.repo = InventoryRepository(db)
    def list(self, model):
        return self.repo.list(model)
    def get(self, model, item_id):
        item = self.repo.get(model, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Record not found")
        return item
    def create(self, model, values):
        if model is Product:
            if not self.repo.get(Category, values["category_id"]):
                raise HTTPException(status_code=400, detail="Category does not exist")
            if values.get("supplier_id") and not self.repo.get(Supplier, values["supplier_id"]):
                raise HTTPException(status_code=400, detail="Supplier does not exist")
        return self.repo.create(model(**values))
    def update(self, model, item_id, values):
        item = self.get(model, item_id)
        if model is Product:
            if values.get("category_id") is not None and not self.repo.get(Category, values["category_id"]):
                raise HTTPException(status_code=400, detail="Category does not exist")
            if values.get("supplier_id") is not None and not self.repo.get(Supplier, values["supplier_id"]):
                raise HTTPException(status_code=400, detail="Supplier does not exist")
        return self.repo.update(item, values)
    def delete(self, model, item_id):
        item = self.get(model, item_id)
        self.repo.delete(item)
