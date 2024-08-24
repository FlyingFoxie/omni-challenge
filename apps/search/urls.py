from django.urls import include, path

from .views import EmployeeListView

app_name = "search"
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
