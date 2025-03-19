from __future__ import annotations

from litestar import Litestar, get
from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import post
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
    base,
    repository,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models.computation import ComputationModel
from backend.schemas.computation import ComputationDB, ComputationCreate
from backend.celery_app import app
from backend.tasks import make_computation




class ComputationRepository(repository.SQLAlchemyAsyncRepository[ComputationModel]):
    """Computation repository."""
    model_type = ComputationModel


async def provide_computation_repo(db_session: AsyncSession) -> ComputationRepository:
    """This provides the default Authors repository."""
    return ComputationRepository(session=db_session)


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
        # Start the Celery task
        task = make_computation.delay(data.title, data.operation, data.a, data.b)
        
        # Return the task ID to the client
        return {"task_id": task.id}

    @get(path='/computations/{computation_id: int}')
    async def get_computation(
        self, computation_id: int, computation_repo: ComputationRepository
        ) -> ComputationDB:
        computation = await computation_repo.get(computation_id)
        return ComputationDB.from_orm(computation)

    @get(path='/computations/status/{task_id: str}')
    async def get_computation_status(
        self, task_id: str
        ) -> dict:
        """Get the status of a computation task."""
        task = make_computation.AsyncResult(task_id)
        return {"status": task.status, "result": task.result}


session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite", session_config=session_config
)  # Create 'db_session' dependency.
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


async def on_startup() -> None:
    """Initializes the database."""
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(base.UUIDBase.metadata.create_all)


app = Litestar(
    route_handlers=[ComputationController],
    on_startup=[on_startup],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
)