from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, DateTime, Integer, JSON, String


class Base(DeclarativeBase):
    pass


class BleEvent(Base):
    __tablename__ = "ble_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(50), default="ble_scan")
    device_address: Mapped[str | None] = mapped_column(String(64), index=True)
    local_name: Mapped[str | None] = mapped_column(String(255))
    rssi: Mapped[int | None] = mapped_column(Integer)
    service_uuids: Mapped[list] = mapped_column(JSON, default=list)
    manufacturer_data: Mapped[dict] = mapped_column(JSON, default=dict)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255))
    device_type: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text)
    last_rssi: Mapped[int | None] = mapped_column(Integer)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    conditions: Mapped[dict] = mapped_column(JSON, default=dict)
    actions: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

class RuleTrigger(Base):
    __tablename__ = "rule_triggers"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, index=True, nullable=False)
    rule_name = Column(String, nullable=False)
    device_address = Column(String, index=True, nullable=False)
    local_name = Column(String, nullable=True)
    rssi = Column(Integer, nullable=True)
    actions = Column(JSON, nullable=False, default=list)
    payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
