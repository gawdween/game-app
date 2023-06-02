# **Introduction**

This is a RESTful API for managing game plays. It allows users to register and login, create playsessions for games, and view a list of games and users.

## Requirements

Python 3.x

Django 3.x

Django Rest Framework 3.x

djangorestframework_simplejwt 4.x

# **Getting Started**

1. [ ] Clone the repository:
   * `git clone https://github.com/yourusername/gameplays-api.git`


2. [ ] Install the requirements:
   * ` pip install -r requirements.txt`


3. [ ] Migrate the database:
   * `python manage.py migrate`


4. [ ] Create a superuser:
    * `python manage.py createsuperuser`


5. [ ] Run Tests:
   * `python manage.py test`


6. [ ] Run the server:
    * `python manage.py runserver`


7. [ ] Access the API at:
     * `http://localhost:8000/`


# **Endpoints**


### **Register a User**

POST /register/

Register a new user. Fields required: email, password, username, and birthdate.

Example Request:

{

    "email": "johndoe@example.com",
    "password": "mypassword123",
    "username": "johndoe",
    "birthdate": "1990-01-01"
}

Example Response:

{

    "user_info": {
        "email": "johndoe@example.com",
        "username": "johndoe",
        "birthdate": "2000-03-20"
    }
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyODQxMzczLCJpYXQiOjE2ODI4NDEwNzMsImp0aSI6IjgxMWFjMmRjMzNkYzRmNTViMjdiMzdhNjkzNTk2YmZmIiwidXNlcl9pZCI6IjNjYjNlZjFiLWE2NzktNGY1OC04MjExLWE2YmQ1YjRhZjVhNCJ9.T9trs5e1s2zmoqGv85EfTNbUI6ssgn2xMChka-wf-iI",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MjkyNzQ3MywiaWF0IjoxNjgyODQxMDczLCJqdGkiOiJkMzQ5ZDExNjIyNDQ0Yzk5OGE3Y2E0YTNiM2JhMDE1YiIsInVzZXJfaWQiOiIzY2IzZWYxYi1hNjc5LTRmNTgtODIxMS1hNmJkNWI0YWY1YTQifQ.fQzpRh0u9tCfimEVQlz5_HF9LiDNeb2tqdLEEVqMtc4",
    
}

### **Login**

POST /login

Get an access token and a refresh token. Fields required: email and password.

Example Request:

{

    "email": "johndoe@example.com",
    "password": "mypassword123"
}

Example Response:

{

    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyODQxMzczLCJpYXQiOjE2ODI4NDEwNzMsImp0aSI6IjgxMWFjMmRjMzNkYzRmNTViMjdiMzdhNjkzNTk2YmZmIiwidXNlcl9pZCI6IjNjYjNlZjFiLWE2NzktNGY1OC04MjExLWE2YmQ1YjRhZjVhNCJ9.T9trs5e1s2zmoqGv85EfTNbUI6ssgn2xMChka-wf-iI",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MjkyNzQ3MywiaWF0IjoxNjgyODQxMDczLCJqdGkiOiJkMzQ5ZDExNjIyNDQ0Yzk5OGE3Y2E0YTNiM2JhMDE1YiIsInVzZXJfaWQiOiIzY2IzZWYxYi1hNjc5LTRmNTgtODIxMS1hNmJkNWI0YWY1YTQifQ.fQzpRh0u9tCfimEVQlz5_HF9LiDNeb2tqdLEEVqMtc4",
    "user_info": {
        "email": "johndoe@example.com",
        "username": "johndoe",
        "birthdate": "2000-03-20"
    }
}

### **List Users**

GET /users/

Retrieve a list of all users. This endpoint is restricted to staff users only.

Example Response:

[

    {
        "id": ce253ba9-ae4e-4819-9056-3261e6ae1e5f,
        "email": "johndoe@example.com",
        "username": "johndoe",
        "birthdate": "1990-01-01",
        "is_active": true
    },
    {
        "id": "3cb3ef1b-a679-4f58-8211-a6bd5b4af5a4",
        "email": "janedoe@example.com",
        "username": "janedoe",
        "birthdate": "1995-01-01",
        "is_active": true
    }
]


### **List Games**

GET /games/

Retrieve a list of all games.

Example Response:


[

    {
        "id": 1,
        "name": "Spiderman",
        "genre": "Action"
    },
    {
        "id": 2,
        "name": "Raider",
        "genre": "Board-game"
    },
    {
        "id": 3,
        "name": "Zuma",
        "genre": "Arcade"
    }
]

### **Get a Specific Game**

GET /games/{id}/

Retrieve a specific game by its id.

Example Response:

{

        "id": 1,
        "name": "Spiderman",
        "genre": "Action"
}

### **Create a Playsession**

POST /playsessions

Create a new playsession. Fields required: user and game.
This endpoint is restricted to authenticated registered users only

Example Request:

{

    "game": 2
}

Example Response:

{

    "id": 1,
    "user": "3cb3ef1b-a679-4f58-8211-a6bd5b4af5a4",
    "game": 2,
    "created_at": "2023-04-30T07:52:17.719542Z"
}