from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column(
        "organization_id",
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "activity_id",
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class OrganizationPhone(Base):
    __tablename__ = "organization_phones_entity"

    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    )
    phone: Mapped[str] = mapped_column(String(32), primary_key=True)

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="phones",
    )


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    building_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
    )

    building: Mapped["Building"] = relationship("Building", back_populates="organizations")

    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary=organization_activities,
        back_populates="organizations",
    )

    phones: Mapped[list[OrganizationPhone]] = relationship(
        "OrganizationPhone",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
