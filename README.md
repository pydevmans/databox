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
  - `post`: creates the <B>databases</B>
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

  `curl http://127.0.0.1:5000/login -X POST -d "username=user2" -d "password=HelloWorld2023!" -v`

- to access protected endpoint
  `curl --cookie "session=<session_key>" http://127.0.0.1:5000/test`
  `document.cookie = "cookie_name=cookie_value"` (in browser's console)

- to logout the user
  `curl http://127.0.0.1:5000/logout`

- to create database
  `curl http://127.0.0.1:5000/users/user2/databases -X POST --cookie "session=<session_key>" -d "title=<title_here>" -d "fields=name:str,dob:str,role:str,emp_no:int,salary:int,phone:int,office:str"`

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

## For performance Testing in Web Browser:

- to get the general idea about request-response timing

`curl http://127.0.0.1:8080`

- Time taken to <i>login</i>

`curl http://127.0.0.1:8080/login -X POST -d "username=user2" -d "password=HelloWorld2023!" -v`

- Time take to access database

`http://127.0.0.1:8080/users/user2/databases`

- Time taken to access small file (`profiles`)

`http://127.0.0.1:8080/users/user2/databases/profiles`

- Time taken for search query parameter

`http://127.0.0.1:8080/users/user2/databases/profiles?page=50&page-size=10`

- Time taken

`http://127.0.0.1:8080/users/user2/databases/profiles?first_name-sw=Lee&age-ge=18&age-le=55&last_name-sw=G&pk-gt=500&pk-le=9975`

Multiple Queries: ~60-70ms
Pagination: 55ms (size=10)
Total access: 108ms
