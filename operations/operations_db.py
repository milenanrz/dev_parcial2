'''Aqui debes construir las operaciones que se te han indicado'''
from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import update
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession


from data.models import EstadoUsuario, UserSQL, EstadoTarea, TaskSQL

#add users
async def create_user_sql(session: Session, user:UserSQL):
    db_user = UserSQL.model_validate(user, from_attributes=True)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user

#show all users
async def get_all_users(session:Session):
    results = await session.exec(select(UserSQL))
    users = results.all()
    return users

#show one user by id
async def get_user(session:Session, user_id:int):
    return await session.get(UserSQL, user_id)

#update user
async def update_user(session:Session, user_id:int, user_update:Dict[str, Any]):
    user = await session.get(UserSQL, user_id)
    if user is None:
        return None

    user_data = user.dict()
    for key, value in user_update.items():
        if value is not None:
            user_data[key]=value


    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

#update user state
async def mark_user_state(session: Session, user_id: int, actual_state:EstadoUsuario):
    return await update_user(session, user_id, {"estado_usuario": actual_state})

#update user premium
async def mark_user_premium(session:Session, user_id:int, user_premium:bool):
    query = (update(UserSQL).where(UserSQL.id == user_id).values(premium=user_premium))
    result = await session.execute(query)
    await session.commit()  # confirma el cambio
    if result.rowcount == 0:  # cuantas filas fueron modificadas
        return False
    return True

#show all inactive users
async def find_user_state(session:Session, user_state:EstadoUsuario = EstadoUsuario.Inactivo):
    query = (select(UserSQL).where(UserSQL.estado_usuario == user_state))
    result = await session.execute(query)
    user = result.scalars().all()
    return user

#show all inactive and premium users
async def find_user_state_and_premium(session:Session, user_state:EstadoUsuario = EstadoUsuario.Inactivo):
    query = (select(UserSQL).where(UserSQL.estado_usuario == user_state, UserSQL.premium == True))
    result = await session.execute(query)
    user = result.scalars().all()
    return user


#add tasks
async def create_task_sql(session: Session, task:TaskSQL):
    db_task = TaskSQL.model_validate(task, from_attributes=True)

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


#show all tasks
async def get_all_tasks(session:Session):
    results = await session.exec(select(TaskSQL))
    tasks = results.all()
    return tasks


#show one task by id
async def get_task(session:Session, task_id:int):
    return await session.get(TaskSQL, task_id)


#update task
async def update_task(session:Session, task_id:int, task_update:Dict[str, Any]):
    task = await session.get(TaskSQL, task_id)
    if task is None:
        return None

    task_data = task.dict()
    for key, value in task_update.items():
        if value is not None:
            task_data[key]=value

    task_data["fecha_modificacion"] = datetime.now()

    for key, value in task_data.items():
        setattr(task, key, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


#update task state
async def mark_task_state(session: Session, task_id: int, actual_state:EstadoTarea):
    return await update_task(session, task_id, {"estado_tarea": actual_state})

