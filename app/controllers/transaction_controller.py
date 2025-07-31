from sqlalchemy.orm import Session
from fastapi import HTTPException

from schemas.transaction_schema import *
from models.user_model import User

def resolve_create_transaction(db: Session, data: TransactionCreate, Transaction, user_data):
    user_email = user_data.get("email")
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_transaction = Transaction(
        amount=data.amount,
        projectKey=data.projectKey,
        type=data.type,
        creationdate=datetime.utcnow(),
        donator=data.donator,
        detalii=data.detalii,
        ownerKey=user.id,
        fromAccount=data.fromAccount,
        toAccount=data.toAccount,
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


def resolve_get_transactions(session: Session, Transaction):
    return session.query(Transaction).all()


def resolve_delete_transaction(session: Session, transaction_id: int, Transaction):
    transaction = session.query(Transaction).get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    session.delete(transaction)
    session.commit()
    return {"message": "Transaction deleted"}