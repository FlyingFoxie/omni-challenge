import random

from django.contrib.auth.models import User
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from apps.search.constants import COLUMN_CHOICES, EMPLOYEE_STATUS_CHOICES
from apps.search.models import Company, Employee, Organization


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = Faker("email")
    password = Faker("password")


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = Faker("company")
    display_columns = random.sample(list(COLUMN_CHOICES.keys()), random.randint(1, 4))
    user = SubFactory(UserFactory)


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Faker("company")
    organization = SubFactory(OrganizationFactory)


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    company = SubFactory(CompanyFactory)
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email_address = Faker("email")
    contact_number = Faker("phone_number")
    department = Faker("word")
    position = Faker("job")
    location = Faker("city")
    status = random.choice([choice[0] for choice in EMPLOYEE_STATUS_CHOICES])
