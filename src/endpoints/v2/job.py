from fastapi import APIRouter, Depends, Path, Query
from src.crud.crud_job import job as crud_job
from src.db.models.job import Job
from sqlalchemy.ext.asyncio import AsyncSession
from src.endpoints.deps import get_db, get_user_id
from fastapi_pagination import Page
from fastapi_pagination import Params as PaginationParams
from pydantic import UUID4
from src.schemas.job import JobType
from typing import List
from datetime import datetime
from src.schemas.common import OrderEnum
router = APIRouter()


@router.get(
    "/{id}",
    response_model=Job,
    response_model_exclude_none=True,
    status_code=201,
)
async def get_job(
    async_session: AsyncSession = Depends(get_db),
    id: UUID4 = Path(
        ...,
        description="The ID of the layer to get",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ),
):
    """Retrieve a job by its ID."""
    job = await crud_job.get(db=async_session, id=id)
    return job

@router.get(
    "",
    response_model=Page[Job],
    response_model_exclude_none=True,
    status_code=201,
)
async def read_jobs(
    async_session: AsyncSession = Depends(get_db),
    page_params: PaginationParams = Depends(),
    user_id: UUID4 = Depends(get_user_id),
    job_type: List[JobType]
    | None = Query(
        None,
        description="Job type to filter by. Can be multiple. If not specified, all job types will be returned.",
    ),
    project_id: UUID4 | None = Query(
        None,
        description="Project ID to filter by. If not specified, all projects will be returned.",
    ),
    start_data: datetime | None = Query(
        None,
        description="Specify the start date to filter the jobs. If not specified, all jobs will be returned.",
    ),
    end_data: datetime | None = Query(
        None,
        description="Specify the end date to filter the jobs. If not specified, all jobs will be returned.",
    ),
    read: bool | None = Query(
        False,
        description="Specify if the job should be read. If not specified, all jobs will be returned.",
    ),
    order_by: str = Query(
        None,
        description="Specify the column name that should be used to order. You can check the Layer model to see which column names exist.",
        example="created_at",
    ),
    order: OrderEnum = Query(
        "descendent",
        description="Specify the order to apply. There are the option ascendent or descendent.",
        example="descendent",
    ),
):
    """Retrieve a list of jobs using different filters."""

    return await crud_job.get_by_date(
        async_session=async_session,
        user_id=user_id,
        page_params=page_params,
        project_id=project_id,
        job_type=job_type,
        start_data=start_data,
        end_data=end_data,
        read=read,
        order_by=order_by,
        order=order,
    )