<h1 align="center">KAMI Airlines</h1>
<p align="center">
    <em>Django framework, airplane fuel consumption analysis</em>
</p>

---

## Table of Contents
1. [Getting Up and Running Locally](#getting-up-and-running-locally)
   1. [Running Test and Coverage Report](#running-test-and-coverage-report)
   2. [Existing Coverage Report in this REPO](#existing-coverage-report-in-this-repo)
2. [Getting Up and Running Locally With Docker](#getting-up-and-running-locally-with-docker)

---

## Getting Up and Running Locally

Prerequisites:

- Python 3.11

sqlite3 database will be used for simplicity of setting up and running locally.

1. Create a virtualenv:
```bash
$ python -m venv <virtual env path>
```

2. Activate the virtualenv you have just created:
```bash
$ source <virtual env path>/bin/activate
```

3. Install local requirements:
```bash
$ pip install -r requirements/local.txt
```

4. Install pre-commit (optional - for development):
```bash
$ pre-commit install
```

5. Apply migrations:
```bash
$ python manage.py migrate
```

6. Run django server:
```bash
$ python manage.py runserver
```

Now that the server's running, visit http://127.0.0.1:8000/ with your web browser. You'll be redirected to the swagger
api docs page.

![API Docs](https://mybucketla.s3.ap-southeast-1.amazonaws.com/Screenshot+2023-11-30+at+8.12.54%E2%80%AFAM.png)

### Running Test and Coverage Report

This project uses the [Pytest](https://docs.pytest.org/en/latest/example/simple.html) for testing. After you have set up
to run locally, run the following commands for testing result:

```bash
$ pytest
```

You can run the `pytest` with code `coverage` by following commands:
```bash
$ coverage run -m pytest
```

Once the tests are complete, run the following commands to see the code coverage:
```bash
$ coverage report
```

### Existing Coverage Report in this REPO
```
Name                                            Stmts   Miss  Cover
-------------------------------------------------------------------
airlines/__init__.py                                0      0   100%
airlines/admin.py                                   3      0   100%
airlines/apps.py                                    4      0   100%
airlines/migrations/0001_initial.py                 5      0   100%
airlines/migrations/__init__.py                     0      0   100%
airlines/models/__init__.py                         1      0   100%
airlines/models/abstracts/time_stamp_model.py       6      0   100%
airlines/models/airplane.py                        12      1    92%
airlines/models/airplane_manager.py                11      0   100%
airlines/serializers/__init__.py                    1      0   100%
airlines/serializers/airplane_serializer.py        18      0   100%
airlines/tests/__init__.py                          0      0   100%
airlines/tests/conftest.py                          8      0   100%
airlines/tests/factories.py                        13      0   100%
airlines/tests/test_drf_views.py                   45      0   100%
airlines/tests/test_models.py                      13      0   100%
airlines/urls.py                                    4      0   100%
airlines/views/__init__.py                          1      0   100%
airlines/views/airplane_viewset.py                 35      0   100%
kami_airlines/__init__.py                           0      0   100%
kami_airlines/settings/base.py                     22      0   100%
kami_airlines/settings/test.py                      1      0   100%
kami_airlines/urls.py                               7      0   100%
-------------------------------------------------------------------
TOTAL                                             210      1    99%
```

---

## Getting Up and Running Locally With Docker

Prerequisites:

- Docker
- Docker Compose

1. Configuring the Environment

You'll need to configure 2 env_file `.django` and `.postgres` in folder .envs/ . Reference can be made from sample folder .envs/.sample .
```
.envs
├── .sample
│   ├── .django
│   └── .postgres
├── .django
└── .postgres
```

2. Build and Run the Stack
```bash
$ docker-compose up -d --build
```

Now that the server's running, visit http://127.0.0.1:8000/ with your web browser. You'll be redirected to the swagger
api docs page.

![API Docs](https://mybucketla.s3.ap-southeast-1.amazonaws.com/Screenshot+2023-11-30+at+8.12.54%E2%80%AFAM.png)
