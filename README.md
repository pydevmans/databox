# Databox Web Application Service

## Running Tests and getting Test Coverage report

    At the project directory level directory run the command,

- `coverage run -m pytest` (to run all tests)
- `coverage report -m` (to generate report in CLI)
- `coverage html` (to generate report in HTML Web Page)

## Sources:

- [Password Encryption Standard](https://www.ibm.com/docs/en/i/7.4?topic=security-password-encryption)

## Ad Hoc commands to get started:

`python -m venv venv`

`python -m pip install --upgrade pip`

`source venv\Script\activate` (for linux) or

`venv\Scripts\activate` (for Win 10)

`python -m pip install -r requirement.txt`

`pip freeze > requirements.txt`

`set FLASK_APP=app.py` (For Win)

`set FLASK_DEBUG=0 or 1`

`export FLASK_APP=app.py` (For Linux)

`export FLASK_DEBUG=0 or 1`

`flask run` (for production)

`flask run --reload --debugger` (for testing)
