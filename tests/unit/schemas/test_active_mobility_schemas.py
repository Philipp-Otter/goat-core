import pytest
from pydantic import ValidationError

from src.schemas.active_mobility import (
    TravelDistanceCostActiveMobility,
    IsochroneStartingPointsActiveMobility,
)

def test_check_starting_points_below_1000():
    # Test with a number of starting points that is below 1000
    try:
        IsochroneStartingPointsActiveMobility(
            latitude=[i % 180 - 90 for i in range(500)], 
            longitude=[i % 360 - 180 for i in range(500)]
        )
    except ValidationError:
        pytest.fail("ValidationError was raised unexpectedly!")

def test_check_starting_points_above_1000():
    # Test with a number of starting points that is above 1000
    with pytest.raises(ValidationError):
        IsochroneStartingPointsActiveMobility(
            latitude=[i % 180 - 90 for i in range(1500)], 
            longitude=[i % 360 - 180 for i in range(1500)]
        )

def test_distance_step_divisible_by_50():
    # Test with a value that is divisible by 50
    try:
        TravelDistanceCostActiveMobility(max_distance=1000, distance_step=100)
    except ValidationError:
        pytest.fail("ValidationError was raised unexpectedly!")

def test_distance_step_not_divisible_by_50():
    # Test with a value that is not divisible by 50
    with pytest.raises(ValidationError):
        TravelDistanceCostActiveMobility(max_distance=1000, distance_step=45)