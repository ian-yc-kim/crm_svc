from .charts import (
    create_sales_performance_chart,
    create_team_productivity_chart,
    create_customer_interaction_chart,
    create_pipeline_analytics_chart,
)
from crm_svc.frontend.components.mobile_components import (
    get_mobile_base_css,
    inject_mobile_base_css,
    inject_viewport_meta,
)

__all__ = [
    "create_sales_performance_chart",
    "create_team_productivity_chart",
    "create_customer_interaction_chart",
    "create_pipeline_analytics_chart",
    "get_mobile_base_css",
    "inject_mobile_base_css",
    "inject_viewport_meta",
]
