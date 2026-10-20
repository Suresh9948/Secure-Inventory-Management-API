from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.inventory import Category, Product, Supplier

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db
    def list(self, model):
        return list(self.db.scalars(select(model).order_by(model.id)))
    def get(self, model, item_id):
        return self.db.get(model, item_id)
    def create(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    def update(self, item, values):
        for key, value in values.items():
            if value is not None or key == "description":
                setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item
    def delete(self, item):
        self.db.delete(item)
        self.db.commit()
