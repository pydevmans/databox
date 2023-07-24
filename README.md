# Databox Web Application Service

## Tests and Test Coverage report

At the project directory level directory run the command,
    
``` sh
coverage run -m pytest
coverage report -m
coverage html
```

## Developer Commands:

``` python3
# Create virtual env and update pip
python3 -m venv venv
python3 -m pip install --upgrade pip

# For Linux
source venv\Script\activate

# For Windows
venv\Scripts\activate
python3 -m pip install -r requirement.txt

# Setting Env Variables For Server
# set <Key>=<Value> (For Win)
# export <Key>=<Value> (For Linux)
DEBUG=0 # or 1
SECRET_KEY
ACCESS_CONTROL_ALLOW_ORIGIN
PYBLOG_API_TOKEN

# Env Var for Github Workflow Automation
GH_ACTION_ROLE
AVAILABILITYZONE

# Env Variables Only for AWS Stack Creation
SECURITYGROUPIDS
IMAGEID
KEYNAME
INSTANCETYPE
SUBNETID
AVAILABILITYZONE

# Env Variables Only for FrontEnd
API_URL

# For Development
python3 app.py
```

## Sources:

- [Password Encryption Standard](https://www.ibm.com/docs/en/i/7.4?topic=security-password-encryption)