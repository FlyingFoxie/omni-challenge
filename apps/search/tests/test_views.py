import pytest
from django.urls import reverse

from apps.search.models import Employee
from apps.search.views import EmployeeListView

pytestmark = pytest.mark.django_db


class TestEmployeeListView:
    def test_employee_list(self, client, random_ip, two_organizations):
        """test employee get request without filtering parameters"""
        client.force_login(two_organizations[0].user)
        response = client.get(
            reverse("search:employee"),
            headers={"X-Forwarded-For": random_ip},
        )

        employee_objects = Employee.objects.filter(
            company__organization=two_organizations[0]
        )
        assert response.status_code == 200
        assert response.json()["count"] == employee_objects.count()

    def test_employee_filtering(self, client, random_ip, two_organizations):
        """test each filtering parameter"""
        employee_object = Employee.objects.filter(
            company__organization=two_organizations[0]
        ).first()
        filtering_params = {
            "company": employee_object.company.id,
            "department": employee_object.department,
            "location": employee_object.location,
            "position": employee_object.position,
            "status": employee_object.status,
        }

        client.force_login(two_organizations[0].user)
        for key, value in filtering_params.items():
            filter_kwargs = {key: value}
            response = client.get(
                reverse("search:employee"),
                filter_kwargs,
                headers={"X-Forwarded-For": random_ip},
            )
            response_data = response.json()
            employee_objects_filtered = (
                Employee.objects.get_list_by_organization_and_filters(
                    two_organizations[0], **filter_kwargs
                )
            )

            assert response.status_code == 200
            assert response_data["count"] == employee_objects_filtered.count()

    def test_employee_filtering_same_company(
        self, client, random_ip, two_organizations
    ):
        """test if there's leakage of data between companies"""
        employee_object = Employee.objects.filter(
            company__organization=two_organizations[0]
        ).first()

        company_id = employee_object.company.id
        filtering_params = {
            "department": employee_object.department,
            "location": employee_object.location,
            "position": employee_object.position,
            "status": employee_object.status,
        }

        client.force_login(two_organizations[0].user)
        for key, value in filtering_params.items():
            filter_kwargs = {"company": company_id, key: value}
            response = client.get(
                reverse("search:employee"),
                filter_kwargs,
                headers={"X-Forwarded-For": random_ip},
            )
            response_data = response.json()
            employee_objects_filtered = (
                Employee.objects.get_list_by_organization_and_filters(
                    two_organizations[0], **filter_kwargs
                )
            )

            assert response.status_code == 200
            assert response_data["count"] == employee_objects_filtered.count()

    def test_dynamic_columns_serializer(self, client, two_organizations, random_ip):
        """test if the dynamic columns are added to the response accordingly"""
        client.force_login(two_organizations[0].user)
        response = client.get(
            reverse("search:employee"),
            headers={"X-Forwarded-For": random_ip},
        )
        response_data = response.json()

        assert response.status_code == 200
        for column in two_organizations[0].display_columns:
            assert column in response_data["results"][0]

    def test_rate_limit(self, client, two_organizations):
        """test rate limit"""
        client.force_login(two_organizations[0].user)
        for _ in range(EmployeeListView.RATE_LIMIT):
            response = client.get(reverse("search:employee"))
            assert response.status_code == 200

        response = client.get(reverse("search:employee"))
        assert response.status_code == 429

    def test_employee_filtering_different_organization(
        self, two_organizations, client, random_ip
    ):
        client.force_login(two_organizations[0].user)
        response = client.get(
            reverse("search:employee"),
            headers={"X-Forwarded-For": random_ip},
        )

        employee_objects = Employee.objects.get_list_by_organization_and_filters(
            two_organizations[0]
        )

        assert response.status_code == 200
        assert response.json()["count"] == employee_objects.count()

    def test_pagination(
        self, client, random_ip, one_organization_one_company_thirty_employees
    ):
        client.force_login(one_organization_one_company_thirty_employees.user)
        response = client.get(
            reverse("search:employee"),
            headers={"X-Forwarded-For": random_ip},
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["next"] is not None

        next_page_response = client.get(
            response_data["next"],
            headers={"X-Forwarded-For": random_ip},
        )
        next_page_response_data = next_page_response.json()
        assert next_page_response.status_code == 200
        assert next_page_response_data["next"] is None
