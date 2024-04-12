from sqlmodel import Field, SQLModel, Column, DateTime, Text
from datetime import datetime

class SystemTaskBase(SQLModel):
    """Base class for system tasks requiring a last run timestamp."""

    id: str = Field(
        sa_column=Column(
            Text,
            nullable=False,
            primary_key=True,
        ),
    )
    last_run: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

class SystemTask(SystemTaskBase, table=True):
    """Table class for system tasks requiring a last run timestamp."""

    __tablename__ = "system_task"
    __table_args__ = {"schema": "customer"}
