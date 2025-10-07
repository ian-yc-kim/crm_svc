import logging
from typing import Dict, List

from plotly import express as px
from plotly import graph_objects as go

from crm_svc.schemas.report import (
    SalesPerformanceResponse,
    TeamProductivityResponse,
    CustomerInteractionResponse,
    PipelineAnalyticsResponse,
)

logger = logging.getLogger(__name__)


def _format_date_range(start, end) -> str:
    try:
        return f"{start} - {end}"
    except Exception:
        return ""


def create_sales_performance_chart(data: SalesPerformanceResponse) -> go.Figure:
    """Create a bar chart summarizing key sales performance metrics.

    Returns a plotly.graph_objects.Figure
    """
    try:
        metrics = ["revenue", "conversion_rate", "pipeline_velocity"]
        values = [data.revenue, data.conversion_rate, data.pipeline_velocity]
        title = f"Sales Performance ({_format_date_range(data.start_date, data.end_date)})"
        fig = px.bar(x=metrics, y=values, labels={"x": "Metric", "y": "Value"}, title=title)
        return fig
    except Exception as e:
        logger.error(e, exc_info=True)
        # fallback empty figure with message
        fig = go.Figure()
        fig.layout.title = "Sales Performance (error generating chart)"
        return fig


def create_team_productivity_chart(data: TeamProductivityResponse) -> go.Figure:
    """Create a team productivity bar chart.

    Returns a plotly.graph_objects.Figure
    """
    try:
        metrics = ["tasks_completed", "deals_closed", "activity_level"]
        values = [data.tasks_completed, data.deals_closed, data.activity_level]
        title = f"Team Productivity ({_format_date_range(data.start_date, data.end_date)})"
        fig = px.bar(x=metrics, y=values, labels={"x": "Metric", "y": "Value"}, title=title)
        return fig
    except Exception as e:
        logger.error(e, exc_info=True)
        fig = go.Figure()
        fig.layout.title = "Team Productivity (error generating chart)"
        return fig


def create_customer_interaction_chart(data: CustomerInteractionResponse) -> go.Figure:
    """Create a customer interaction bar chart.

    Returns a plotly.graph_objects.Figure
    """
    try:
        metrics = ["total_interactions", "avg_engagement_score"]
        values = [data.total_interactions, data.avg_engagement_score]
        title = f"Customer Interaction ({_format_date_range(data.start_date, data.end_date)})"
        fig = px.bar(x=metrics, y=values, labels={"x": "Metric", "y": "Value"}, title=title)
        return fig
    except Exception as e:
        logger.error(e, exc_info=True)
        fig = go.Figure()
        fig.layout.title = "Customer Interaction (error generating chart)"
        return fig


def create_pipeline_analytics_chart(data: PipelineAnalyticsResponse) -> go.Figure:
    """Create a pipeline analytics chart (bar) for stage conversion rates.

    Returns a plotly.graph_objects.Figure
    """
    try:
        stages: Dict[str, float] = data.stage_conversion_rates or {}
        title = f"Pipeline Analytics ({_format_date_range(data.start_date, data.end_date)})"
        if not stages:
            fig = go.Figure()
            fig.layout.title = "Pipeline Analytics (no data)"
            return fig
        names: List[str] = list(stages.keys())
        rates: List[float] = [stages[k] for k in names]
        fig = px.bar(x=names, y=rates, labels={"x": "Stage", "y": "Conversion Rate"}, title=title)
        return fig
    except Exception as e:
        logger.error(e, exc_info=True)
        fig = go.Figure()
        fig.layout.title = "Pipeline Analytics (error generating chart)"
        return fig
