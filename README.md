# Databox Web Application Service

## Tests and Test Coverage report

At the project directory level directory run the command,
    
``` bash
coverage run -m pytest
coverage report -m
coverage html
```

## Create virtual env, update pip and install dependencies:

``` python
python3 -m venv venv
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```


## Activating Virtual Env

``` python
# For Linux
source venv\Script\activate

# For Windows
venv\Scripts\activate
```

## Environment Variable Setup
``` bash
# set <Key>=<Value> (For Windows OS)
# export <Key>=<Value> (For Linux OS)

# Environment Variable for Backend Server
ACCESS_CONTROL_ALLOW_ORIGIN
DEBUG=0 # or 1
PYBLOG_API_TOKEN
SALT
SECRET_KEY

# Environment Variable for Github Workflow Automation
ACCESS_CONTROL_ALLOW_ORIGIN
DEBUG=0 # or 1
PYBLOG_API_TOKEN
SALT
SECRET_KEY

# Environment Variable Only for AWS Stack Creation
AVAILABILITYZONE
GH_ACTION_ROLE
IMAGEID
KEYNAME
INSTANCETYPE
SECURITYGROUPIDS
SUBNETID

# Environment Variable Only for FrontEnd
API_URL
```

## For Development
``` python
python3 app.py
```

## Sources:

- [Password Encryption Standard](https://www.ibm.com/docs/en/i/7.4?topic=security-password-encryption)