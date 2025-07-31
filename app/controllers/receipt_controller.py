from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.receipt_schema import *

def resolve_create_receipt(session: Session, data: ReceiptCreate, Receipt):
    new_receipt = Receipt(**data.dict())
    session.add(new_receipt)
    session.commit()
    session.refresh(new_receipt)
    return new_receipt

def resolve_get_receipts(session: Session, Receipt):
    return session.query(Receipt).all()


def resolve_delete_receipt(session: Session, receipt_id: int, Receipt):
    receipt = session.query(Receipt).get(receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    session.delete(receipt)
    session.commit()
    return {"message": "Receipt deleted"}