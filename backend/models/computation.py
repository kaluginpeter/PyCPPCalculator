import enum

from sqlalchemy.orm import Mapped
from sqlalchemy import Column, String, Text, Enum, Integer
from litestar.plugins.sqlalchemy import base


class Operation(enum.StrEnum):
    ADDITION = 'addition'


class ComputationModel(base.UUIDBase):
    """
    Describe instance of computation process.
    """
    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String(512), name='Title of computation')
    operation: Mapped[Operation] = Column(Enum(Operation))
    result: Mapped[str] = Column(Text, name='Result of computation')