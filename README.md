# Databox Web Application Service

## Purpose

    This web application allows user to create the relations database and perform aggregation operation on it through web interface.

## Features

    - Ceate, Delete, Update and Read Relation Database
    - a monitor to maintain the size of the database to the optimal size and perform necessary rebuilts.
    - Scalable in term of divide and conquer technique to perform aggregation in reasonable time
        + leverage the multi-process to do all aggregation
        + provide API to access the data fetched/aggregated
    - Live testable on machine in containerised format
    - testable code which assesses the func upon all the commits made to the branch `testing`
    - CI/CD implementation
    - DevOps implemented

## Flow of the Code

    Feature branch ---> Testing branch ---> Master branch

## Running Tests

    At the project directory level directory run the command,

`py -m unittest backend\test_core.py`

# Implement Web Interface

## Features

- serves through web interface and api endpoints
- user login and password protection access
- create the sophisticated HTML, css page, run it with Flask
- Front End (Vue):
  - / (landing/info page)
  - /login
  - /signup
  - /forget_password (L)
  - /features
  - /username (L)
    - list all the database
  - /username/database (L)
    - list records (view only)
    - append records
  - /username/database/pk_record (L)
    - view the greyout form with option to edit
    - TBD update the record

* (L) means Locked access. Valid credentials are needed.

- Back End (flask):
  - serves through all web request and direct backend request through api
  - for API access, different protection mechanism has to be generated.
- ## Microservice based:
  - have 2 containers running, Vue and Flask. Vue serves the page and Flask serves the data.
  - Have 2 different endpoint (production and testing)
  - upon pushing code to testing, testing endpoint should run all the testing and if successful, have web access. If error is found generate logs to specific file.
  - if testing is all good, can be pushed to production.
  -

## Sources:

- [Password Encryption Standard](https://www.ibm.com/docs/en/i/7.4?topic=security-password-encryption)

## List of Commands:

`python3 -m venv venv`

`source venv\Script\activate` (for linux) or

`venv\Scripts\activate` (for Win 10)

`pip install -r requirement.txt`

`pip freeze > requirements.txt`

`set FLASK_APP=app.py`

`set FLASK_DEBUG=0 or 1`

`flask run` (for production)

`flask run --reload --debugger` (for testing)
