import random

import pytest

from .factories import CompanyFactory, EmployeeFactory, OrganizationFactory


@pytest.fixture
def random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


@pytest.fixture
def two_organizations():
    organizations = OrganizationFactory.create_batch(2)
    companies_organizations_a = CompanyFactory.create_batch(
        2, organization=organizations[0]
    )
    companies_organizations_b = CompanyFactory.create_batch(
        2, organization=organizations[1]
    )

    for company in companies_organizations_a:
        EmployeeFactory.create_batch(random.randint(1, 10), company=company)

    for company in companies_organizations_b:
        EmployeeFactory.create_batch(random.randint(1, 10), company=company)

    return organizations
