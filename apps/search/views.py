from datetime import timedelta

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.search.services.filters import employee_filter
from apps.search.services.limiters import CustomRateLimit
from apps.search.services.paginations import CustomPageNumberPagination

from .constants import EMPLOYEE_STATUS_CHOICES
from .models import Employee
from .serializers import EmployeeQuerySerializer, EmployeeSerializer


@extend_schema(
    tags=["employees"],
    parameters=[
        OpenApiParameter(
            name="company", description="Filter by company ID", required=False, type=int
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
    queryset = Employee.objects.all().order_by("first_name")
    serializer_class = EmployeeSerializer
    pagination_class = CustomPageNumberPagination
    rate_limit_class = CustomRateLimit

    RATE_LIMIT = 10  # Number of allowed requests
    TIME_PERIOD = timedelta(minutes=1)  # Time period for rate limiting

    def get(self, request, *args, **kwargs):
        rate_limiter = self.rate_limit_class(self.RATE_LIMIT, self.TIME_PERIOD)

        if rate_limiter.is_rate_limited(request):
            return Response(
                {"detail": "Rate limit exceeded. Try again later."}, status=429
            )

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        serializer = EmployeeQuerySerializer(data=self.request.query_params)
        if serializer.is_valid():
            queryset = employee_filter(queryset, **serializer.validated_data)

        return queryset
