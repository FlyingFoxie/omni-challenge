from rest_framework import serializers

from .constants import EMPLOYEE_STATUS_CHOICES
from .models import Company, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ["id", "company", "created_datetime", "updated_datetime"]


class EmployeeQuerySerializer(serializers.Serializer):
    """
    Serializer for filtering employees in request query params
    """

    status = serializers.ChoiceField(choices=EMPLOYEE_STATUS_CHOICES, required=False)
    location = serializers.CharField(max_length=100, required=False)
    position = serializers.CharField(max_length=100, required=False)
    department = serializers.CharField(max_length=100, required=False)
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), required=False
    )
