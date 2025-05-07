'''Aqui debes consignar el modelo que se te indico en el parcial
Escribe aquí el que te corresponde.

'''
from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class EstadoUsuario(Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Eliminado = "Eliminado"


class UserBase(SQLModel):
    nombre: Optional[str] = Field(min_length=3, max_length=20)
    email: Optional[str] = Field(min_length=10, max_length=50)
    estado_usuario: Optional[EstadoUsuario] = Field(default=EstadoUsuario.Activo)
    premium: Optional[bool] = Field(default=False)

class UserSQL(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    model_config = ConfigDict(from_attributes=True)

class EstadoTarea(Enum):
    Pendiente = "Pendiente"
    En_ejecucion = "En ejecución"
    Realizada = "Realizada"
    Cancelada = "Cancelada"

class TaskBase(SQLModel):
    nombre: Optional[str] = Field(min_length=3, max_length=20)
    descripcion: Optional[str] = Field(min_length=3, max_length=100)
    estado_tarea: Optional[EstadoTarea] = Field(default=EstadoTarea.Pendiente)
    fecha_creacion: Optional[datetime] = Field(default_factory=datetime.now)
    fecha_modificacion: Optional[datetime] = Field(default_factory=datetime.now)
    usuario_id: int = Field(foreign_key="users.id")

class TaskSQL(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)

    model_config = ConfigDict(from_attributes=True)

