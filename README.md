<h1 align="center">OMNI Employee Search Microservice</h1>
<p align="center">
    <em>Built with django rest framework</em>
</p>

---

## Table of Contents
1. [About](#about)
2. [Getting Up and Running Locally](#getting-up-and-running-locally)
   1. [Running Test and Coverage Report](#running-test-and-coverage-report)
3. [Getting Up and Running Locally With Docker](#getting-up-and-running-locally-with-docker)
4. [Existing Coverage Report in this REPO](#existing-coverage-report-in-this-repo)

---

## About

This microservice provides an API endpoint for listing employees within an organization. The primary goal is to allow
users to retrieve employee data efficiently based on various criteria.

The EmployeeListView endpoint supports several query parameters:

1. **company**: Filters the employee list by the company's UUID.
2. **status**: Filters the employee list by their employment status.
3. **location**: Filters the employee list by location.
4. **position**: Filters the employee list by job position.
5. **department**: Filters the employee list by department.

## Getting Up and Running Locally

To set up the local development environment with all necessary dependencies, run the following command in your virtual
environment :
```bash
$ poetry install --with dev
```
If you do not have Poetry installed, you can follow the [Poetry installation guide](https://python-poetry.org/docs/#installation)
to get it set up on your system.

**(Optional)** After initializing your Git repository, you can optionally set up a pre-commit hook to automatically format
and lint your code before each commit. .
```bash
$ pre-commit install
```

Apply migrations and run django server. (sqlite3 database will be used for simplicity of setting up and running locally)
```bash
$ python manage.py migrate
$ python manage.py runserver
```

Now that the server's running, visit http://127.0.0.1:8000/ with your web browser. You'll be redirected to the [swagger
api docs page](http://127.0.0.1:8000/api/docs).

### Running Test and Coverage Report

This project uses the [Pytest](https://docs.pytest.org/en/latest/example/simple.html) for testing. After you have set up
to run locally, run the following commands for testing result:

```bash
$ make coverage_report
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
$ make docker_build
```

Once the build is complete, visit http://127.0.0.1:8000/ with your web browser. You'll be redirected to the [swagger
api docs page](http://127.0.0.1:8000/api/docs).

### Running Test and Coverage Report

Run the `make` command to test and generate coverage report.

```Bash
$ make docker_django_coverage_report
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
