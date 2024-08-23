from django.urls import include, path

from .views import EmployeeListView

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("employee/", EmployeeListView.as_view(), name="employee"),
            ]
        ),
    )
]
