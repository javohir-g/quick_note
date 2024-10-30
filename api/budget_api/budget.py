from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel

from database.models import engine
from database.budgetservice import BudgetService

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()


class BudgetBase(BaseModel):
    category: str
    amount: float


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int
    date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/budgets/", response_model=List[Budget])
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    budgets = BudgetService.get_budgets(db, skip=skip, limit=limit)
    return budgets


@router.post("/budgets/", response_model=Budget)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    return BudgetService.create_budget(db=db, category=budget.category, amount=budget.amount)


@router.get("/budgets/{budget_id}", response_model=Budget)
def read_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = BudgetService.get_budget(db, budget_id=budget_id)
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.put("/budgets/{budget_id}", response_model=Budget)
def update_budget(budget_id: int, budget: BudgetCreate, db: Session = Depends(get_db)):
    updated_budget = BudgetService.update_budget(
        db=db, budget_id=budget_id, category=budget.category, amount=budget.amount
    )
    if updated_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return updated_budget


@router.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = BudgetService.delete_budget(db=db, budget_id=budget_id)
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"message": "Budget deleted successfully"}