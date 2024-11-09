# utils.py
from sqlalchemy.exc import IntegrityError
from fastapi_async_sqlalchemy import db
from fastapi import HTTPException
from database import User
from sqlalchemy import select, update, insert, delete  # Import select from sqlalchemy


async def profile_query(email):
        commandstmt = select(User).where(User.email == email)
        result = await commandfunc(commandstmt)
        user = result.scalar_one_or_none()  # Get the user or None
        return user

async def profile_command(email,phone):
    stmt = update(User).where(User.email == email).values(phone=phone)
    result = await db.session.execute(stmt)
    await db.session.commit()
    return result

async def commandfunc(commandstmt):
        try:
            result = await db.session.execute(commandstmt)
        except IntegrityError:
            db.session.rollback()
            raise HTTPException(status_code=400, detail="An error occurred. This record may already exist.")
        return result


# async def exec(email):
#     async with db():
#         commandstmt = select(User).where(email)
#         result = await commandfunc(commandstmt)
#         user = result.scalar_one_or_none()  # Get the user or None
#         return user
    

    # async with db():
        
    #      stmt = update(User).where(User.email == user_info_auth.email).values(phone=phone)
    #      result = await db.session.execute(stmt)
    #      await db.session.commit()


    #     # Use select from sqlalchemy to create the query
    #      stmt = select(User).where(User.email == user_info_auth.email)
    #      result = await db.session.execute(stmt)
    #      user = result.scalar_one_or_none()  # Get the user or None
        
 

# async def exec(email):
#     async with db():
#         # Use select from sqlalchemy to create the query
#         stmt = select(User).where(User.email == email)
#         result = await db.session.execute(stmt)
#         user = result.scalar_one_or_none()  # Get the user or None
#         return user