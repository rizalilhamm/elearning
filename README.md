# ELECTRONIC MOBILE LEARNING
The Repository is built to complete one of Information Technology Departmant for Electronic Mobile Learning Course

```
git clone https://github.com/rizalilhamm/elearning.git
```
## Installation
Before you run bellow intructions make sure you have made your virtual Enviroment and activeted 

```bash
pip install -r requirements.txt
export FLASK_APP=elearning
flask run
```
# REST API
The REST API Electronic Mobile Learning Described below. You can test it using Postman
### Authentication
include Register, Login, Logout
``` base
127.0.0.1:5000/account/register
    
127.0.0.1:5000/account/login
    
127.0.0.1:5000/account/logout
```

### Class Service
Get All Class
```base
    127.0.0.1:5000/classes
```
Get a particular Class
```base
    127.0.0.1:5000/classes/<int:id>
```