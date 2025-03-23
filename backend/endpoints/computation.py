from litestar import Controller, get, post
from litestar.exceptions import ValidationException
from litestar.di import Provide
from sqlalchemy import select

from backend.schemas.computation import ComputationDB, ComputationCreate
from backend.models.computation import ComputationModel
from backend.repositories.computation import (
    ComputationRepository, provide_computation_repo
)
from backend.celery.tasks import make_computation


class ComputationController(Controller):
    """Computation CRUD"""
    dependencies = {"computation_repo": Provide(provide_computation_repo)}

    @get(path="/computations")
    async def list_computations(
        self,
        computation_repo: ComputationRepository,
    ) -> list[ComputationDB]:
        """List computations."""
        computations = await computation_repo.session.execute(select(ComputationModel))
        return [ComputationDB.from_orm(obj) for obj in computations.scalars().all()]

    @post(path="/computations")
    async def create_computation(
        self,
        computation_repo: ComputationRepository,
        data: ComputationCreate,
    ) -> dict:
        """Create a new computation."""
        task = make_computation.delay(data.title, data.operation, data.operand_a, data.operand_b)
        computation = ComputationModel(**data.dict())
        computation.task_id = task.id
        await computation_repo.add(computation)
        await computation_repo.session.commit()
        return {"task_id": task.id} 

    @get(path='/computations/{computation_id: int}')
    async def get_computation(
        self, computation_id: int, computation_repo: ComputationRepository
        ) -> ComputationDB:
        computation = await computation_repo.get(computation_id)
        return ComputationDB.from_orm(computation)

    @get(path='/computations/status/{task_id: str}')
    async def get_computation_status(
        self, 
        task_id: str, 
        computation_repo: ComputationRepository
    ) -> dict:
        """Get the status of a computation task."""
        task = make_computation.AsyncResult(task_id) 
        if isinstance(task.result, dict) and task.result.get('Error'):
            computation = await computation_repo.get_by_task_id(task_id)
            if computation:
                await computation_repo.session.delete(computation)
                await computation_repo.session.commit()
            raise ValidationException(task.result.get('Error'))
        
        if task.successful():
            computation = await computation_repo.get_by_task_id(task_id)
            computation.result = task.result
            await computation_repo.add(computation)
            await computation_repo.session.commit()
            await computation_repo.session.refresh(computation)
            
            if computation:
                return {
                    "status": task.status,
                    "result": ComputationDB.from_orm(computation).dict()
                }
            else:
                return {"status": task.status, "error": "Computation not found in database"}
        else:
            return {"status": task.status, "error": str(task.result)}