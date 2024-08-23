from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView

from .constants import EMPLOYEE_STATUS_CHOICES
from .filters import employee_filter
from .models import Employee
from .paginations import CustomPageNumberPagination
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

    def get_queryset(self):
        queryset = super().get_queryset()

        serializer = EmployeeQuerySerializer(data=self.request.query_params)
        if serializer.is_valid():
            queryset = employee_filter(queryset, **serializer.validated_data)

        return queryset
