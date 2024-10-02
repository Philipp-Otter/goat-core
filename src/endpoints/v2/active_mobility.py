from fastapi import APIRouter, Body, Depends

from src.core.tool import start_calculation
from src.crud.crud_catchment_area import CRUDCatchmentAreaActiveMobility
from src.crud.crud_heatmap_closest_average import CRUDHeatmapClosestAverage
from src.crud.crud_heatmap_connectivity import CRUDHeatmapConnectivity
from src.crud.crud_heatmap_gravity import CRUDHeatmapGravity
from src.deps.auth import auth_z
from src.endpoints.deps import get_http_client
from src.schemas.catchment_area import (
    ICatchmentAreaActiveMobility,
)
from src.schemas.catchment_area import (
    request_examples_catchment_area_active_mobility as active_mobility_request_examples,
)
from src.schemas.heatmap import (
    IHeatmapClosestAverageActive,
    IHeatmapConnectivityActive,
    IHeatmapGravityActive,
)
from src.schemas.job import JobType
from src.schemas.toolbox_base import CommonToolParams, IToolResponse

router = APIRouter()


@router.post(
    "/catchment-area",
    summary="Compute catchment areas for active mobility",
    response_model=IToolResponse,
    status_code=201,
    dependencies=[Depends(auth_z)],
)
async def compute_active_mobility_catchment_area(
    *,
    common: CommonToolParams = Depends(),
    params: ICatchmentAreaActiveMobility = Body(
        ...,
        examples=active_mobility_request_examples["catchment_area_active_mobility"],
        description="The catchment area parameters.",
    ),
):
    """Compute catchment areas for active mobility."""

    return await start_calculation(
        job_type=JobType.catchment_area_active_mobility,
        tool_class=CRUDCatchmentAreaActiveMobility,
        crud_method="run_catchment_area",
        async_session=common.async_session,
        user_id=common.user_id,
        background_tasks=common.background_tasks,
        project_id=common.project_id,
        params=params,
        http_client=get_http_client(),
    )


@router.post(
    "/heatmap-gravity",
    summary="Compute heatmap gravity for active mobility",
    response_model=IToolResponse,
    status_code=201,
    dependencies=[Depends(auth_z)],
)
async def compute_active_mobility_heatmap_gravity(
    *,
    common: CommonToolParams = Depends(),
    params: IHeatmapGravityActive = Body(
        ...,
        examples={},
        description="The heatmap gravity parameters.",
    ),
):
    """Compute heatmap gravity for active mobility."""

    return await start_calculation(
        job_type=JobType.heatmap_gravity_active_mobility,
        tool_class=CRUDHeatmapGravity,
        crud_method="run_heatmap",
        async_session=common.async_session,
        user_id=common.user_id,
        background_tasks=common.background_tasks,
        project_id=common.project_id,
        params=params,
    )


@router.post(
    "/heatmap-closest-average",
    summary="Compute heatmap closest-average for active mobility",
    response_model=IToolResponse,
    status_code=201,
    dependencies=[Depends(auth_z)],
)
async def compute_active_mobility_heatmap_closest_average(
    *,
    common: CommonToolParams = Depends(),
    params: IHeatmapClosestAverageActive = Body(
        ...,
        examples={},
        description="The heatmap closest-average parameters.",
    ),
):
    """Compute heatmap closest-average for active mobility."""

    return await start_calculation(
        job_type=JobType.heatmap_closest_average_active_mobility,
        tool_class=CRUDHeatmapClosestAverage,
        crud_method="run_heatmap",
        async_session=common.async_session,
        user_id=common.user_id,
        background_tasks=common.background_tasks,
        project_id=common.project_id,
        params=params,
    )


@router.post(
    "/heatmap-connectivity",
    summary="Compute heatmap connectivity for active mobility",
    response_model=IToolResponse,
    status_code=201,
    dependencies=[Depends(auth_z)],
)
async def compute_active_mobility_heatmap_connectivity(
    *,
    common: CommonToolParams = Depends(),
    params: IHeatmapConnectivityActive = Body(
        ...,
        examples={},
        description="The heatmap connectivity parameters.",
    ),
):
    """Compute heatmap connectivity for active mobility."""

    return await start_calculation(
        job_type=JobType.heatmap_connectivity_active_mobility,
        tool_class=CRUDHeatmapConnectivity,
        crud_method="run_heatmap",
        async_session=common.async_session,
        user_id=common.user_id,
        background_tasks=common.background_tasks,
        project_id=common.project_id,
        params=params,
    )
