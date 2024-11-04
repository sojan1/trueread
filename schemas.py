from typing import List
from pydantic import BaseModel, constr
class UserSchema(BaseModel):
   id: int
   username: str
   email:str
   password: str
   name:str
   phone: str
   class Config:
      orm_mode = True