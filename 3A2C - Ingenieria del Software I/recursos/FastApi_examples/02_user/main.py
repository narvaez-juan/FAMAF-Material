from typing import Optional
from fastapi import FastAPI, HTTPException, status
from users import USERS, get_user_by_id
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserIn(BaseModel):
    name: str
    surname: str
    age: Optional[int] = None
    mail: EmailStr
    active: bool

class UserOut(BaseModel):
    id: int
    name: str
    operation_result: str

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    res_user = None
    res_user = get_user_by_id(user_id=user_id)
    if not res_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="user not found"
        )
    return res_user
 
@app.get("/users/")
async def get_user_list(
    user_from: Optional[int] = 0, 
    user_to: Optional[int] = None
):
    return USERS[user_from:user_to]

@app.post(
    "/users/", 
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def create_user(new_user: UserIn) -> int:
    new_id = len(USERS) + 1
    user_dict = new_user.dict()
    user_dict.update({"id": new_id})
    USERS.append(user_dict)
    return UserOut(
        id=new_id, 
        name=new_user.name, 
        operation_result="Succesfully created!")

