from uuid import UUID

from pydantic import BaseModel as _BaseModel

from backend.models.computation import Operation


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""
    class Config:
        from_attributes = True
        orm_mode = True


class ComputationDB(BaseModel):
    id: int
    title: str
    operation: Operation
    result: str


class ComputationCreate(BaseModel):
    title: str
    operation: Operation
    result: str
    a: float
    b: float
