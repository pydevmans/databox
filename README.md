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

`coverage run -m pytest` (to run all tests)
`coverage report -m` (to generate report in CLI)
`coverage html` (to generate report in HTML Web Page)

# Implement Web Interface

## Features

- serves through web interface and api endpoints
- user login and password protection access
- create the sophisticated HTML, css page, run it with Flask
- Front End (Vue):

  - / (landing/info page)
  - /login
  - /signup
  - /forget_password
  - /features
  - /users/`<username:str>`
    - list all the database
  - /users/`<username:str>`/profile
    - list user's info
  - /users/`<username:str>`/databases
  - /users/`<username:str>`/databases/`<database:str>`
    - list records (view only)
    - append records
  - /users/`<username:str>`/databases/`<database:str>`/pk_record
    - view the greyout form with option to edit
    - TBD update the record

## Testing commands

- to sign up user

  `curl http://127.0.0.1:5000/signup -d "first_name=test" -d "last_name=tetly" -d "membership=1" -d "username=user1" -d "email_address=user1@icloud.com" -d "password=HelloWorld2023!"`

- to login user

  `curl http://127.0.0.1:5000/login -X POST -d "username=rj9" -d "password=HelloWorld1!" -v`

- to access protected endpoint
  `curl --cookie "session=<session_key>" http://127.0.0.1:5000/test`
  `document.cookie = "cookie_name=cookie_value"` (in browser's console)

- to logout the user
  `curl http://127.0.0.1:5000/logout`

Back End (flask):

- serves through all web request and direct backend request through api
- for API access, different protection mechanism has to be generated.

## Microservice based:

- have 2 containers running, Vue and Flask. Vue serves the page and Flask serves the data.
- Have 2 different endpoint (production and testing)
- upon pushing code to testing, testing endpoint should run all the testing and if successful, have web access. If error is found generate logs to specific file.
- if testing is all good, can be pushed to production.
-

## Sources:

- [Password Encryption Standard](https://www.ibm.com/docs/en/i/7.4?topic=security-password-encryption)

## Ad Hoc commands to get started:

`python -m venv venv`

`python -m pip install --upgrade pip`

`source venv\Script\activate` (for linux) or

`venv\Scripts\activate` (for Win 10)

`python -m pip install -r requirement.txt`

`pip freeze > requirements.txt`

`set FLASK_APP=app.py`

`set FLASK_DEBUG=0 or 1`

`flask run` (for production)

`flask run --reload --debugger` (for testing)
