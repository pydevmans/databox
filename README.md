# Databox Web Application Service

## Running Tests and getting Test Coverage report

    At the project directory level directory run the command,

- `coverage run -m pytest` (to run all tests)
- `coverage report -m` (to generate report in CLI)
- `coverage html` (to generate report in HTML Web Page)

## API End points:

- /
  - `get`: List all the features of the Service
- /signup
  - `post`: Pass (first_name, last_name, membership, username, email_address, password) to sign up.
- /login
  - `post`: Pass (username, password) to login to account
  <!-- - /forget_password -->
- /logout
  - `post`: To log the user out
- /features
  - `get`: Lists features of 3 Membership types.

### User specific:

- /users/`<username:str>`/profile
  - `get`: list user's info
- /users/`<username:str>`/databases
  - `get`: list all the database
  - `delete`: delete all the <B>databases</B>
- /users/`<username:str>`/databases/`<database:str>`
  - `get`: list records (view only)
    - Apply Pagination and all sorts of URL Query Parameter Operations
  - `put`: rename the `database`
  - `delete`: delete the `database`
- /users/`<username:str>`/databases/`<database:str>`/pk_record
  - `get`: returns the specified record of the database
  - `delete`: deletes the specified record from the database

## Testing commands

- to sign up user

  `curl http://127.0.0.1:5000/signup -d "first_name=test" -d "last_name=tetly" -d "membership=1" -d "username=user1" -d "email_address=user1@icloud.com" -d "password=HelloWorld2023!"`

- to login user

  `curl http://127.0.0.1:5000/login -X POST -d "username=user0" -d "password=HelloWorld2023!" -v`

- to access protected endpoint
  `curl --cookie "session=<session_key>" http://127.0.0.1:5000/test`
  `document.cookie = "cookie_name=cookie_value"` (in browser's console)

- to logout the user
  `curl http://127.0.0.1:5000/logout`

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
