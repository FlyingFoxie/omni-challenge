from django.db import models
from django.db.models import Q


class EmployeeManager(models.Manager):
    def get_list_by_organization_and_filters(self, organization, **kwargs):
        filters = Q()

        field_mappings = {
            "company": "company",
            "status": "status",
            "location": "location__icontains",
            "position": "position__icontains",
            "department": "department__icontains",
        }

        for field, lookup in field_mappings.items():
            value = kwargs.get(field)
            if value:
                filters &= Q(**{lookup: value})

        return self.filter(filters, company__organization=organization).order_by(
            "first_name"
        )
