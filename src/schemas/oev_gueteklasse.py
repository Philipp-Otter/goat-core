from typing import List

from pydantic import BaseModel, Field
from src.schemas.layer import ToolType
from src.schemas.toolbox_base import (
    PTTimeWindow,
    input_layer_type_polygon,
    DefaultResultLayerName,
)
from src.schemas.colors import ColorRangeType


class OevGueteklasseStationConfig(BaseModel):
    groups: dict = Field(
        ...,
        title="Groups",
        description="The groups of the station config.",
    )
    time_frequency: List[int] = Field(
        ...,
        title="Time Frequency",
        description="The time frequency of the station config.",
    )
    categories: List[dict] = Field(
        ...,
        title="Categories",
        description="The categories of the station config.",
    )
    classification: dict = Field(
        ...,
        title="Classification",
        description="The classification of the station config.",
    )


class IOevGueteklasse(BaseModel):
    reference_area_layer_project_id: int = Field(
        ...,
        title="The layer project serving reference Area for the calculation.",
        description="The reference area of the ÖV-Güteklasse.",
    )
    time_window: PTTimeWindow = Field(
        ...,
        title="Time Window",
        description="The time window of the ÖV-Güteklasse.",
    )
    station_config: OevGueteklasseStationConfig = Field(
        ...,
        title="Station Config",
        description="The station config of the ÖV-Güteklasse.",
    )

    @property
    def tool_type(self):
        return ToolType.oev_gueteklasse

    @property
    def input_layer_types(self):
        return {"reference_area_layer_project_id": input_layer_type_polygon}

    @property
    def geofence_table(self):
        return "basic.geofence_pt"


# Check for extended route_type defintion: https://developers.google.com/transit/gtfs/reference/extended-route-types
station_config_example = {
    "groups": {
        "0": "B",
        "1": "A",
        "2": "A",
        "3": "C",
        "7": "B",
        "100": "A",
        "101": "A",
        "102": "A",
        "103": "A",
        "104": "A",
        "105": "A",
        "106": "A",
        "107": "A",
        "108": "A",
        "109": "A",
        "110": "A",
        "111": "A",
        "112": "A",
        "114": "A",
        "116": "A",
        "117": "A",
        "200": "C",
        "201": "C",
        "202": "C",
        "204": "C",
        "400": "A",
        "401": "A",
        "402": "A",
        "403": "A",
        "405": "A",
        "700": "C",
        "701": "C",
        "702": "C",
        "704": "C",
        "705": "C",
        "712": "C",
        "715": "C",
        "800": "C",
        "900": "B",
        "901": "B",
        "902": "B",
        "903": "B",
        "904": "B",
        "905": "B",
        "906": "B",
        "1400": "B",
    },
    "time_frequency": [0, 4, 10, 19, 39, 60, 119],
    "categories": [
        {
            "A": 1,  # i.e. types of transports in category A are in transport stop category I
            "B": 1,
            "C": 2,
        },
        {"A": 1, "B": 2, "C": 3},
        {"A": 2, "B": 3, "C": 4},
        {"A": 3, "B": 4, "C": 5},
        {"A": 4, "B": 5, "C": 6},
        {"A": 5, "B": 6, "C": 7},
    ],
    "classification": {
        "1": {300: "1", 500: "1", 750: "2", 1000: "3", 1250: "4"},
        "2": {300: "1", 500: "2", 750: "3", 1000: "4", 1250: "5"},
        "3": {300: "2", 500: "3", 750: "4", 1000: "5", 1250: "6"},
        "4": {300: "3", 500: "4", 750: "5", 1000: "6", 1250: "6"},
        "5": {300: "4", 500: "5", 750: "6"},
        "6": {300: "5", 500: "6"},
        "7": {300: "6"},
    },
}


request_example_oev_gueteklasse = {
    "oev_gueteklasse_weekday": {
        "summary": "ÖV-Güteklassen Weekday",
        "value": {
            "time_window": {"weekday": "weekday", "from_time": 25200, "to_time": 32400},
            "reference_area_layer_project_id": "1",
            "station_config": station_config_example,
        },
    },
    "oev_gueteklasse_saturday": {
        "summary": "ÖV-Güteklassen Saturday",
        "value": {
            "time_window": {
                "weekday": "saturday",
                "from_time": 25200,
                "to_time": 32400,
            },
            "reference_area_layer_project_id": "1",
            "station_config": station_config_example,
        },
    },
}


oev_gueteklasse_station_config_layer_base = {
    "name": "ÖV-Güteklassen stations",
    "description": "ÖV-Güteklassen Categories on the station level",
    "type": "feature",
    "feature_layer_geometry_type": "point",
    "indicator_type": "oev_gueteklasse",
    "thumbnail_url": "https://goat-app-assets.s3.eu-central-1.amazonaws.com/logos/goat_green.png",
    "style": {},
    "data_source": "Plan4Better GmbH",
    "attribute_mapping": {
        "stop_id": "text_attr1",
        "stop_name": "text_attr2",
        "frequency": "float_attr1",
        "_class": "integer_attr1",
        "trip_cnt": "jsonb_attr1",
        "trip_ids": "jsonb_attr2",
    },
}

oev_gueteklasse_config_layer_base = {
    "name": "ÖV-Güteklassen",
    "description": "ÖV-Güteklassen with catchment areas",
    "layer_type": "feature_layer_type",
    "indicator_type": "oev_gueteklasse",
    "thumbnail_url": "https://goat-app-assets.s3.eu-central-1.amazonaws.com/logos/goat_green.png",
    "style": {},
    "data_source": "Plan4Better GmbH",
}
