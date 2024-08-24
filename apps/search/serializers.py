from rest_framework import serializers

from .constants import EMPLOYEE_STATUS_CHOICES
from .models import Company, Employee


def dynamic_columns_serializer(dynamic_columns: list, serializer):
    class DynamicColumnsSerializer(serializer):
        class Meta(serializer.Meta):
            fields = dynamic_columns + serializer.Meta.fields

    return DynamicColumnsSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email_address", "contact_number"]


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
