from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List
from uuid import UUID

from geoalchemy2 import Geometry
from pydantic import create_model
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlmodel import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Field,
    Float,
    ForeignKey,
    Index,
    Integer,
    Relationship,
    SQLModel,
    Text,
    text,
)

from ._base_class import DateTimeBase

if TYPE_CHECKING:
    from ._link_model import ScenarioScenarioFeatureLink
    from .layer import Layer


class ScenarioFeatureEditType(str, Enum):
    """Edit types."""

    new = "n"
    modified = "m"
    deleted = "d"


def generate_field_definitions():
    field_definitions = {
        "geom": (
            str,
            Field(
                sa_column=Column(
                    Geometry,
                    nullable=False,
                )
            ),
        ),
    }

    for i in range(1, 26):
        field_definitions[f"integer_attr{i}"] = (
            int | None,
            Field(sa_column=Column(Integer)),
        )
        field_definitions[f"float_attr{i}"] = (
            float | None,
            Field(sa_column=Column(Float)),
        )
        field_definitions[f"text_attr{i}"] = (
            str | None,
            Field(sa_column=Column(Text)),
        )

    for i in range(1, 6):
        field_definitions[f"bigint_attr{i}"] = (
            int | None,
            Field(sa_column=Column(BigInteger)),
        )

    for i in range(1, 11):
        field_definitions[f"jsonb_attr{i}"] = (
            dict | None,
            Field(sa_column=Column(JSONB)),
        )
        field_definitions[f"boolean_attr{i}"] = (
            bool | None,
            Field(sa_column=Column(Boolean)),
        )

    for i in range(1, 4):
        field_definitions[f"arrint_attr{i}"] = (
            List[int] | None,
            Field(sa_column=Column(ARRAY(Integer))),
        )
        field_definitions[f"arrfloat_attr{i}"] = (
            List[float] | None,
            Field(sa_column=Column(ARRAY(Float))),
        )
        field_definitions[f"arrtext_attr{i}"] = (
            List[str] | None,
            Field(sa_column=Column(ARRAY(Text))),
        )
        field_definitions[f"timestamp_attr{i}"] = (
            datetime | None,
            Field(sa_column=DateTime(timezone=False)),
        )

    return field_definitions


UserData = create_model("UserData", __base__=SQLModel, **generate_field_definitions())


class ScenarioFeature(DateTimeBase, UserData, table=True):
    """Layer model."""

    __tablename__ = "scenario_feature"
    __table_args__ = {"schema": "customer"}

    id: UUID | None = Field(
        sa_column=Column(
            UUID_PG(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=text("uuid_generate_v4()"),
        )
    )
    feature_id: int | None = Field(
        sa_column=Column(Integer, nullable=True),
        description="Feature ID of the modified feature",
    )
    layer_id: str = Field(
        sa_column=Column(
            UUID_PG(as_uuid=True),
            ForeignKey("customer.layer.id", ondelete="CASCADE"),
            nullable=False,
        ),
        description="Layer ID of the modified layer",
    )
    edit_type: ScenarioFeatureEditType = Field(
        sa_column=Column(Text, nullable=False), description="Type of the edit"
    )
    # Relationships
    original_layer: "Layer" = Relationship(back_populates="scenario_features")

    scenarios_links: List["ScenarioScenarioFeatureLink"] = Relationship(
        back_populates="scenario_feature"
    )


Index(
    "scenario_feature_geom_idx",
    ScenarioFeature.__table__.c.geom,
    postgresql_using="gist",
)
