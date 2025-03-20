import enum

from sqlalchemy.orm import Mapped
from sqlalchemy import Column, String, Text, Enum, Integer
from litestar.plugins.sqlalchemy import base


class Operation(enum.StrEnum):
    """
    Enum string class, that define type of opeartion.
    Uses in database representation of operation in computation.s
    """
    ADDITION = 'addition'
    SUBTRACTION = 'subtraction'
    MULTIPLICATION = 'multiplication'
    DIVISION = 'division'


class ComputationModel(base.UUIDBase):
    """
    Describe instance of computation process.
    """
    id: Mapped[int] = Column(
        Integer, primary_key=True, name='Primary identificator of a model'
    )
    title: Mapped[str] = Column(String(512), name='Title of computation')
    operation: Mapped[Operation] = Column(
        Enum(Operation), name='Describe type of operation from enum class'
    )
    operand_a: Mapped[str] = Column(String, name='First operand of the expression')
    operand_b: Mapped[str] = Column(String, name='Second operand of the expression')
    result: Mapped[str] = Column(
        Text, name='Result of computation', default='Not finished yet!'
    )
    task_id: Mapped[str] = Column(
        Integer, nullable=False, name='Represent id of background task'
    )