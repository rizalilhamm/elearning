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
``` base
127.0.0.1:5000/account/register
    
127.0.0.1:5000/account/login
    
127.0.0.1:5000/account/logout
```
#### User access
1. Register with institution email
    > Lecturer (example@lecture.ar-raniry.ac.id) **(lecture after @)**
    > Student (example@student.ar-raniry.ac.id) **(student after @)**
2. Login with registered email
3. Logout from system
### Class Service
```base
127.0.0.1:5000/classes

127.0.0.1:5000/classes/<int:id>
```
#### Lecturer access
1. Get all classes or particular class
2. Create new Class
3. Update a particular classname
4. Add new student to a particular class
#### Student access
1. Get all classes or particular class

### Tasks Service
```bash
127.0.0.1:5000/classes/<int:id>/tasks

127.0.0.1:5000/classes/<int:id>/tasks/<int:index>
```
#### Lecturer access
1. Get all tasks or a particular task
2. Create new task
3. Update a particular task title

#### Student access
1. Get all tasks or particular task
2. Post Task Response (cancel not allowed after submit)

### Class Material
```bash
127.0.0.1:5000/classes/<int:id>/new_materials
``` 
#### Lecturer access
1. Post new material for a particular class

127.0.0.1:5000/classes/<int:id>/participants/<int:index>
```   
