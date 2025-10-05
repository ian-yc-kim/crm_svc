from datetime import date

import pytest
from pydantic import ValidationError

from crm_svc.schemas.report import (
    DateRangeQuery,
    ReportTypeFilter,
    SalesPerformanceResponse,
)


def test_date_range_query_valid_and_invalid():
    valid = DateRangeQuery.model_validate({"start_date": date(2025, 1, 1), "end_date": date(2025, 1, 2)})
    assert valid.start_date <= valid.end_date

    with pytest.raises(ValidationError):
        DateRangeQuery.model_validate({"start_date": date(2025, 2, 1), "end_date": date(2025, 1, 1)})


def test_response_models_serialization_roundtrip():
    sp = SalesPerformanceResponse(
        start_date=date(2025, 6, 1),
        end_date=date(2025, 6, 3),
        revenue=3000.0,
        conversion_rate=0.05,
        pipeline_velocity=1.23,
    )
    dumped = sp.model_dump()
    recovered = SalesPerformanceResponse.model_validate(dumped)
    assert recovered.revenue == sp.revenue


def test_report_type_filter_values():
    assert ReportTypeFilter.SALES.value == "sales"
    assert ReportTypeFilter.TEAM.value == "team"
    assert ReportTypeFilter.PIPELINE.value == "pipeline"
    assert ReportTypeFilter.CUSTOMER.value == "customer"
