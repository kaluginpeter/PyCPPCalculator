from litestar.plugins.sqlalchemy import repository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.computation import ComputationModel


class ComputationRepository(repository.SQLAlchemyAsyncRepository[ComputationModel]):
    """
    Repository for ComputationModel.
    Define CRUD operations with sqlalchemy model.
    """
    model_type = ComputationModel
    async def get_by_task_id(self, task_id: str) -> ComputationModel:
        """Fetch a computation by its task ID."""
        result = await self.session.execute(
            select(ComputationModel).where(ComputationModel.task_id == task_id)
        )
        return result.scalars().first()


async def provide_computation_repo(db_session: AsyncSession) -> ComputationRepository:
    """
    This provides the computation repository.
    Should use in dependecy injection.
    """
    return ComputationRepository(session=db_session)