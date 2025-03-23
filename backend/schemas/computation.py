from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import Field

from backend.models.computation import Operation
from backend.core.config import settings


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""
    class Config:
        from_attributes = True
        orm_mode = True


class ComputationDB(BaseModel):
    """
    Represent instance of computation as it represent in database.
    """
    id: int
    title: str
    operation: Operation
    result: str
    operand_a: str
    operand_b: str


class ComputationCreate(BaseModel):
    """
    Uses for creating computation.
    """
    title: str
    operation: Operation
    operand_a: float
    operand_b: float
