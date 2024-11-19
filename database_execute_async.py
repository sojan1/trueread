# utils.py
from sqlalchemy.exc import IntegrityError
from fastapi_async_sqlalchemy import db
from fastapi import HTTPException
from database import User
from sqlalchemy import select, update, insert, delete  # Import select from sqlalchemy


async def profile_query(email):
        commandstmt = select(User).where(User.email == email)
        result = await db.session.execute(commandstmt)
        user = result.scalar_one_or_none()  # Get the user or None
        return user

async def profile_command(email,phone):
    stmt = update(User).where(User.email == email).values(phone=phone)
    result = await db.session.execute(stmt)
    await db.session.commit()
    return result


# async def wallet_command(email,phone):
#     stmt = update(User).where(User.email == email).values(phone=phone)
#     result = await db.session.execute(stmt)
#     await db.session.commit()
#     return result
