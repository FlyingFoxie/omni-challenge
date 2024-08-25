<h1 align="center">OMNI Employee Search Microservice</h1>
<p align="center">
    <em>Built with django rest framework</em>
</p>

---

## Table of Contents
1. [About](#about)
   1. [Technologies Used](#technologies-used)
2. [Getting Up and Running Locally](#getting-up-and-running-locally)
   1. [Running Test and Coverage Report](#running-test-and-coverage-report)
3. [Getting Up and Running Locally With Docker](#getting-up-and-running-locally-with-docker)
   1. [Running Test and Coverage Report With Docker](#running-test-and-coverage-report-with-docker)
4. [Existing Coverage Report in this REPO](#existing-coverage-report-in-this-repo)
5. [Development](#development)

---

## About

This microservice provides an API endpoint for listing employees within an organization. The primary goal is to allow
users to retrieve employee data efficiently based on various criteria.

The `/api/v1/employee/` endpoint supports several query parameters:

1. **company**: Filters the employee list by the company's UUID.
2. **status**: Filters the employee list by their employment status.
3. **location**: Filters the employee list by location.
4. **position**: Filters the employee list by job position.
5. **department**: Filters the employee list by department.

### Technologies Used

- API Server: [Django REST Framework](https://www.django-rest-framework.org/)
- Testing: [pytest](https://pytest.org/)
- Linting: black, flake8, isort

## Getting Up and Running Locally

To set up the local development environment with all necessary dependencies, run the following command in your virtual
environment :
```bash
poetry install --with dev
```
If you do not have Poetry installed, you can follow the [Poetry installation guide](https://python-poetry.org/docs/#installation)
to get it set up on your system.

**(Optional)** After initializing your Git repository, you can optionally set up a pre-commit hook to automatically format
and lint your code before each commit. .
```bash
pre-commit install
```

Apply migrations and run django server. (sqlite3 database will be used for simplicity of setting up and running locally)
```bash
python manage.py migrate
python manage.py runserver
```

Now that the server's running, visit http://127.0.0.1:8000/ with your web browser. You'll be redirected to the [swagger
api docs page](http://127.0.0.1:8000/api/docs).

To test the API endpoint, create a superuser to obtain auth-token and authorize in the Swagger Docs, or simply login the
django admin.
```bash
python manage.py createsuperuser
```

### Running Test and Coverage Report

This project uses the [Pytest](https://docs.pytest.org/en/latest/example/simple.html) for testing. After you have set up
to run locally, run the following commands for testing result:

```bash
make coverage_report
```

---

## Getting Up and Running Locally With Docker

Prerequisites:

- Docker
- Docker Compose

If you do not have Docker installed, you can follow the [Docker installation guide](https://docs.docker.com/get-docker/)

Before building and running the stack, you'll need to configure 2 env_file `.django` and `.postgres` in folder .envs/ .
Reference can be made from sample folder .envs/.sample .
```
.envs
├── .sample
│   ├── .django
│   └── .postgres
├── .django
└── .postgres
```

Once the environment files are configures, run the `make` command to build and run the stack.
```bash
make docker_build
```

Once the build is complete, visit http://127.0.0.1:8000/ with your web browser. You'll be redirected to the [swagger
api docs page](http://127.0.0.1:8000/api/docs).

To test the API endpoint, create a superuser to obtain auth-token and authorize in the Swagger Docs, or simply login the
django admin.
```bash
make docker_django_createsuperuser
```

### Running Test and Coverage Report With Docker

Run the `make` command to test and generate coverage report.

```Bash
make docker_django_coverage_report
```

## Existing Coverage Report in this REPO
```
Name                                                                     Stmts   Miss  Cover
--------------------------------------------------------------------------------------------
apps/__init__.py                                                             0      0   100%
apps/search/__init__.py                                                      0      0   100%
apps/search/admin.py                                                        14      0   100%
apps/search/apps.py                                                          4      0   100%
apps/search/constants.py                                                     2      0   100%
apps/search/migrations/0001_initial.py                                       8      0   100%
apps/search/migrations/0002_remove_company_display_columns_and_more.py       4      0   100%
apps/search/migrations/__init__.py                                           0      0   100%
apps/search/model_managers.py                                               11      0   100%
apps/search/models.py                                                       37      3    92%
apps/search/serializers.py                                                  18      0   100%
apps/search/services/__init__.py                                             0      0   100%
apps/search/services/limiters.py                                            34      0   100%
apps/search/services/paginations.py                                          6      0   100%
apps/search/tests/__init__.py                                                0      0   100%
apps/search/tests/conftest.py                                               22      0   100%
apps/search/tests/factories.py                                              35      0   100%
apps/search/tests/test_views.py                                             68      0   100%
apps/search/urls.py                                                          4      0   100%
apps/search/views.py                                                        30      2    93%
omni/__init__.py                                                             0      0   100%
omni/settings/base.py                                                       24      0   100%
omni/settings/test.py                                                        1      0   100%
omni/urls.py                                                                13      1    92%
--------------------------------------------------------------------------------------------
TOTAL                                                                      335      6    98%

```

## Development

### 1. Custom limiters

Custom limiters was used instead of django rest framework built in limiters.

```python
from apps.search.services.limiters import CustomRateLimit, rate_limit

class EmployeeListView(ListAPIView):
    rate_limit_class = CustomRateLimit

    RATE_LIMIT = 10  # Number of allowed requests
    TIME_PERIOD = timedelta(minutes=1)  # Time period for rate limiting
   ...
    @rate_limit(rate_limit_class, RATE_LIMIT, TIME_PERIOD)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

```

This limiter throttle 10 requests per minute based on ip address.
```python
class CustomRateLimit:
    ...
     def is_rate_limited(self, request):
        """Check if rate limit is exceeded"""
        client_ip = self.get_client_ip(request)
        cache_key = f"rl:{client_ip}"
        request_times = cache.get(cache_key, [])

        request_times = [
            t for t in request_times if t > timezone.now() - self.time_period
        ]

        if len(request_times) >= self.rate_limit:
            return True

        request_times.append(timezone.now())
        cache.set(cache_key, request_times, self.time_period.total_seconds())
        return False
```
