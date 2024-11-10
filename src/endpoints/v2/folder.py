from typing import List

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    status,
)
from pydantic import UUID4
from sqlalchemy import func, select

from src.core.config import settings
from src.crud.crud_folder import folder as crud_folder
from src.db.models.folder import Folder
from src.db.session import AsyncSession
from src.deps.auth import auth_z
from src.endpoints.deps import get_db, get_user_id
from src.schemas.common import OrderEnum
from src.schemas.folder import (
    FolderCreate,
    FolderRead,
    FolderUpdate,
)
from src.schemas.folder import (
    request_examples as folder_request_examples,
)

router = APIRouter()


### Folder endpoints
@router.post(
    "",
    summary="Create a new folder",
    response_model=FolderRead,
    status_code=201,
    dependencies=[Depends(auth_z)],
)
async def create_folder(
    *,
    async_session: AsyncSession = Depends(get_db),
    user_id: UUID4 = Depends(get_user_id),
    folder_in: FolderCreate = Body(..., example=folder_request_examples["create"]),
):
    """Create a new folder."""
    # Count already existing folders for the user
    folder_cnt = await async_session.execute(
        select(func.count(Folder.id)).filter(Folder.user_id == user_id)
    )
    folder_cnt = folder_cnt.scalar()

    # Check if the user has already reached the maximum number of folders
    if folder_cnt >= settings.MAX_FOLDER_COUNT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"The maximum number of folders ({settings.MAX_FOLDER_COUNT}) has been reached.",
        )

    folder_in.user_id = user_id
    folder = await crud_folder.create(async_session, obj_in=folder_in)
    return folder


@router.get(
    "/{folder_id}",
    summary="Retrieve a folder by its ID",
    response_model=FolderRead,
    status_code=200,
    dependencies=[Depends(auth_z)],
)
async def read_folder(
    *,
    async_session: AsyncSession = Depends(get_db),
    user_id: UUID4 = Depends(get_user_id),
    folder_id: UUID4 = Path(
        ...,
        description="The ID of the folder to get",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ),
):
    """Retrieve a folder by its ID."""
    folder = await crud_folder.get_by_multi_keys(
        async_session, keys={"id": folder_id, "user_id": user_id}
    )

    if len(folder) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
        )

    return folder[0]


@router.get(
    "",
    summary="Retrieve a list of folders",
    response_model=List[FolderRead],
    response_model_exclude_none=True,
    status_code=200,
    dependencies=[Depends(auth_z)],
)
async def read_folders(
    *,
    async_session: AsyncSession = Depends(get_db),
    user_id: UUID4 = Depends(get_user_id),
    search: str = Query(None, description="Searches the name of the folder"),
    order_by: str = Query(
        None,
        description="Specify the column name that should be used to order. You can check the Project model to see which column names exist.",
        example="created_at",
    ),
    order: OrderEnum = Query(
        "descendent",
        description="Specify the order to apply. There are the option ascendent or descendent.",
        example="descendent",
    ),
):
    """Retrieve a list of folders."""
    query = select(Folder).where(Folder.user_id == user_id)
    folders = await crud_folder.get_multi(
        async_session,
        query=query,
        search_text={"name": search} if search else {},
        order_by=order_by,
        order=order,
    )
    folders = [folder[0] for folder in folders]

    return folders


@router.put(
    "/{folder_id}",
    summary="Update a folder with new data",
    response_model=FolderUpdate,
    status_code=200,
    dependencies=[Depends(auth_z)],
)
async def update_folder(
    *,
    async_session: AsyncSession = Depends(get_db),
    folder_id: UUID4 = Path(
        ...,
        description="The ID of the folder to update",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ),
    user_id: UUID4 = Depends(get_user_id),
    folder_in: FolderUpdate = Body(..., example=folder_request_examples["update"]),
):
    """Update a folder with new data."""
    db_obj = await crud_folder.get_by_multi_keys(
        async_session, keys={"id": folder_id, "user_id": user_id}
    )

    if len(db_obj) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
        )

    folder = await crud_folder.update(async_session, db_obj=db_obj[0], obj_in=folder_in)
    return folder


@router.delete(
    "/{folder_id}",
    summary="Delete a folder and all its contents",
    response_model=None,
    status_code=204,
    dependencies=[Depends(auth_z)],
)
async def delete_folder(
    *,
    async_session: AsyncSession = Depends(get_db),
    folder_id: UUID4 = Path(
        ...,
        description="The ID of the folder to delete",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ),
    user_id: UUID4 = Depends(get_user_id),
    background_tasks: BackgroundTasks,
):
    """Delete a folder and all its contents"""

    await crud_folder.delete(
        async_session, background_tasks=background_tasks, id=folder_id, user_id=user_id
    )
    return
