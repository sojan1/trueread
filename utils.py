# utils.py
from sqlalchemy.exc import IntegrityError
from fastapi_sqlalchemy import db
from fastapi import HTTPException
from sqlalchemy import select
from database import User



def add_to_database(instance):
    """Add an instance to the database session and commit it."""
    try:
        db.session.add(instance)
        db.session.commit()
        db.session.refresh(instance)
        return instance
    except IntegrityError:
        db.session.rollback()
        raise HTTPException(status_code=400, detail="An error occurred. This record may already exist.")
