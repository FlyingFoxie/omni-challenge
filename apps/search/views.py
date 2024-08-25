from datetime import timedelta
from uuid import UUID

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from apps.search.services.limiters import CustomRateLimit, rate_limit
from apps.search.services.paginations import CustomPageNumberPagination

from .constants import EMPLOYEE_STATUS_CHOICES
from .models import Employee
from .serializers import (
    EmployeeQuerySerializer,
    EmployeeSerializer,
    dynamic_columns_serializer,
)


@extend_schema(
    tags=["employees"],
    parameters=[
        OpenApiParameter(
            name="company",
            description="Filter by company ID",
            required=False,
            type=UUID,
        ),
        OpenApiParameter(
            name="status",
            description="Filter by status",
            required=False,
            type=str,
            enum=[choice[0] for choice in EMPLOYEE_STATUS_CHOICES],
        ),
        OpenApiParameter(
            name="location", description="Filter by location", required=False, type=str
        ),
        OpenApiParameter(
            name="position", description="Filter by position", required=False, type=str
        ),
        OpenApiParameter(
            name="department",
            description="Filter by department",
            required=False,
            type=str,
        ),
    ],
)
class EmployeeListView(ListAPIView):
    serializer_class = EmployeeSerializer
    pagination_class = CustomPageNumberPagination
    rate_limit_class = CustomRateLimit

    RATE_LIMIT = 10  # Number of allowed requests
    TIME_PERIOD = timedelta(minutes=1)  # Time period for rate limiting

    @rate_limit(rate_limit_class, RATE_LIMIT, TIME_PERIOD)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        serializer = EmployeeQuerySerializer(data=self.request.query_params)
        if serializer.is_valid():
            queryset = Employee.objects.get_list_by_organization_and_filters(
                self.request.user.organizations.first(), **serializer.validated_data
            )
        else:
            raise ValidationError(serializer.errors)

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            return self.serializer_class
        else:
            return dynamic_columns_serializer(
                self.request.user.organizations.first().display_columns,
                self.serializer_class,
            )
