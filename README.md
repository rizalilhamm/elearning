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
#### Lecture acces
1. Post new material for a particular class

### Class Participants 
```
127.0.0.1:5000/classes/<int:id>/participants/<int:index>
```   
#### Lecturer access
1. Get all participants or a particular
2. Add new Participants

#### Student access
1. Get all participants 

### Input Score by Lecturer
```bash
http://127.0.0.1:5000/classes/1/tasks/1/answers

http://127.0.0.1:5000/classes/1/tasks/1/answers/<int:index>
```

#### Lecturer access
1. Get all answers or particular answer
2. Check a particular score and appraisal it
3. Ability to update the appraisal

### Comment Service
```bash
Class commments
http://127.0.0.1:5000/classes/1/comments

Task comments
http://127.0.0.1:5000/classes/1/tasks/1/comments
```

#### Lecturer access
1. Ability to post a comment
2. Ability to get all comment

#### Student access
1. Ability to post a comment
2. Ability to get all comment