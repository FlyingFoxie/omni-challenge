import uuid

from django.db import models

from .constants import EMPLOYEE_STATUS_CHOICES


class TimestampedModel(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    display_columns = models.JSONField(default=list)

    def __str__(self):
        return self.name


class Employee(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name="employees"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    contact_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(
        max_length=12, choices=EMPLOYEE_STATUS_CHOICES, default="ACTIVE"
    )

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"
