from fastapi import FastAPI, HTTPException
import uvicorn
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: Optional[str]
    password: str

class UserInput(BaseModel):
    name: str
    email: Optional[str]
    password: str

users = [
    User(id=1, name='Mikhail', email='Mikhail@mail.ru',password='qwerty')
]

@app.get("/")
async def root():
    return {"message": "Users"}

@app.get("/users")
async def get_tasks():
    return users

@app.get('/users/{user_id}', response_model=User)
async def one_user(user_id: int):
    if len(users) < user_id:
        raise HTTPException(status_code=404, detail='User not found')
    return users[user_id - 1]

@app.post("/users", response_model=list[User])
async def new_user(user: UserInput):
    user = User(
        id=len(users) + 1,
        name=user.name,
        email=user.email,
        password=user.password
    )
    users.append(user)
    return users

@app.put('/users/{user_id}', response_model=User)
async def modify(user_id: int, new_user: UserInput):
    for user in users:
        if user.id == user_id:
            user.name = new_user.name
            user.email = new_user.email
            user.password = new_user.password
            return user
        raise HTTPException(status_code=404, detail='User not found')
    
@app.delete('/users/{user_id}', response_model=str)
async def remove_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return f'User deleted'
        raise HTTPException(status_code=404, detail='User not found')

if __name__ == '__main__':
    uvicorn.run('app01:app', host="127.0.0.1", port=8000, reload=True)
    