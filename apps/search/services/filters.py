from django.db.models import Q, QuerySet


def employee_filter(queryset: QuerySet, **kwargs) -> QuerySet:
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

    return queryset.filter(filters)
