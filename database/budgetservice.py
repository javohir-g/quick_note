from sqlalchemy.orm import Session
from . import models
from datetime import datetime


class BudgetService:
    @staticmethod
    def get_budgets(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Budget).offset(skip).limit(limit).all()

    @staticmethod
    def get_budget(db: Session, budget_id: int):
        return db.query(models.Budget).filter(models.Budget.id == budget_id).first()

    @staticmethod
    def create_budget(db: Session, category: str, amount: float):
        budget = models.Budget(category=category, amount=amount)
        db.add(budget)
        db.commit()
        db.refresh(budget)
        return budget

    @staticmethod
    def update_budget(db: Session, budget_id: int, category: str, amount: float):
        budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
        if budget:
            budget.category = category
            budget.amount = amount
            budget.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(budget)
        return budget

    @staticmethod
    def delete_budget(db: Session, budget_id: int):
        budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
        if budget:
            db.delete(budget)
            db.commit()
        return budget