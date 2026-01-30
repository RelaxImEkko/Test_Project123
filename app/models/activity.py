from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("activities.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ограничение на 3 уровня будем делать логикой при создании
    parent: Mapped["Activity | None"] = relationship(
        "Activity",
        remote_side="Activity.id",
        back_populates="children",
    )
    children: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities",
    )
