from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, Form
from sqlmodel import Session

from data.models import UserSQL, EstadoUsuario, TaskSQL, EstadoTarea
from utils.connection_db import init_db, get_session
import operations.operations_db as crud


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


#add users
@app.post("/users", response_model=UserSQL, tags=["USERS"])
async def create_user(nombre: str = Form(...), email: Optional[str] = Form(None),
    estado_usuario: Optional[EstadoUsuario] = Form(None),
    premium: Optional[bool] = Form(default=False),
    session: Session = Depends(get_session)
):

    user_data=UserSQL(
        nombre=nombre,
        email=email,
        estado_usuario=estado_usuario,
        premium=premium
    )
    return await crud.create_user_sql(session, user_data)


#show one user by id
@app.get("/users/{user_id}", response_model=UserSQL, tags=["USERS"])
async def read_user(user_id:int, session:Session = Depends(get_session)):
    return await crud.get_user(session=session, user_id=user_id)


#Get all users
@app.get("/allusers", response_model=list[UserSQL], tags=["USERS"])
async def read_users(session:Session = Depends(get_session)):
    return await crud.get_all_users(session=session)


#Update one user
@app.patch("/users/{user_id}", response_model=UserSQL, tags=["USERS"])
async def update_user(user_id:int, user_update:UserSQL, session:Session=Depends(get_session)):
    return await crud.update_user(session, user_id, user_update.dict(exclude_unset=True))


#user state
@app.patch("/users_state/{user_id}", response_model=UserSQL, tags=["USERS"])
async def change_state(user_id:int, actual_state:EstadoUsuario, session:Session=Depends(get_session)):
    return await crud.mark_user_state(session, user_id, actual_state)


#user premium
@app.patch("/users_premium/{user_id}", response_model=UserSQL, tags=["USERS"])
async def change_premium(user_id:int, user_premium:bool, session:Session=Depends(get_session)):
    return await crud.mark_user_premium(session, user_id, user_premium)


#get all inactive users
@app.get("/users_inactive", response_model=list[UserSQL], tags=["USERS"])
async def find_inactive_users(session:Session=Depends(get_session)):
    return await crud.find_user_state(session)


#get all inactive and premium users
@app.get("/inactive_and_premium_users", response_model=list[UserSQL], tags=["USERS"])
async def find_inactive_and_premium(session:Session=Depends(get_session)):
    return await crud.find_user_state_and_premium(session)

#add tasks
@app.post("/tasks", response_model=TaskSQL, tags=["TASKS"])
async def create_task(nombre: str = Form(...), descripcion: Optional[str] = Form(None),
    estado_tarea: Optional[EstadoTarea] = Form(None),
    session: Session = Depends(get_session)
):

    task_data=TaskSQL(
        nombre=nombre,
        descripcion=descripcion,
        estado_tarea=estado_tarea
    )
    return await crud.create_task_sql(session, task_data)


#show one task by id
@app.get("/tasks/{task_id}", response_model=TaskSQL, tags=["TASKS"])
async def read_task(task_id:int, session:Session = Depends(get_session)):
    return await crud.get_task(session=session, task_id=task_id)


#Get all task
@app.get("/alltasks", response_model=list[TaskSQL], tags=["TASKS"])
async def read_tasks(session:Session = Depends(get_session)):
    return await crud.get_all_tasks(session=session)


#Update one task
@app.patch("/tasks/{task_id}", response_model=TaskSQL, tags=["TASKS"])
async def update_task(task_id:int, task_update:TaskSQL, session:Session=Depends(get_session)):
    return await crud.update_task(session, task_id, task_update.dict(exclude_unset=True))


#task state
@app.patch("/tasks_state/{task_id}", response_model=TaskSQL, tags=["TASKS"])
async def change_tasks_state(task_id:int, actual_state:EstadoTarea, session:Session=Depends(get_session)):
    return await crud.mark_task_state(session, task_id, actual_state)