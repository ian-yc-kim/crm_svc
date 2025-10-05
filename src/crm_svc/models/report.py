import uuid
from datetime import datetime, date

from sqlalchemy import Column, String, Date, DateTime, Integer, Float, JSON as SA_JSON
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import TypeDecorator

from .base import Base


class JSONBCompatible(TypeDecorator):
    """Dialect-aware JSONB type: use PostgreSQL JSONB when available, otherwise JSON.

    This ensures compatibility with both PostgreSQL and SQLite.
    """
    impl = SA_JSON

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(postgresql.JSONB())
        return dialect.type_descriptor(SA_JSON())


class SalesPerformanceMetrics(Base):
    __tablename__ = "sales_performance_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    revenue = Column(Float, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    pipeline_velocity = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<SalesPerformanceMetrics(id={self.id}, start_date={self.start_date}, end_date={self.end_date})>"


class TeamProductivityMetrics(Base):
    __tablename__ = "team_productivity_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    tasks_completed = Column(Integer, nullable=False)
    deals_closed = Column(Integer, nullable=False)
    activity_level = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<TeamProductivityMetrics(id={self.id}, tasks_completed={self.tasks_completed})>"


class CustomerInteractionMetrics(Base):
    __tablename__ = "customer_interaction_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_interactions = Column(Integer, nullable=False)
    avg_engagement_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<CustomerInteractionMetrics(id={self.id}, total_interactions={self.total_interactions})>"


class PipelineAnalyticsMetrics(Base):
    __tablename__ = "pipeline_analytics_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    # store a mapping stage -> conversion rate
    stage_conversion_rates = Column(JSONBCompatible(), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<PipelineAnalyticsMetrics(id={self.id}, stages={self.stage_conversion_rates})>"
