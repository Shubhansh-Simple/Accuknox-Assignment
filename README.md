
# Accuknox-Assignment

## Let's get started
This is a social media application (Backend) built with Django & Django Rest Framework


### Features/Functionalities
- Create User
- User Authorization
- Add Friends
- View Friends
- Search for Users


### Installation
- Clone the repo from your terminal/cmd using the command: ```https://github.com/Shubhansh-Simple/Accuknox-Assignment.git```
- Make sure you have Docker installed in your local system.

If you do not have Docker installed in your system, you can still run the same with the commands below.
- Create a virtual Environment
- Install the required libraries and modules: ```pip3 install -r requirements.txt```
- Populate the .env file with the below configuration.
  Example:
  ```
  DEBUG=True
  SECRET_KEY='Your secret_key here'
  ```

- Also, Create a new DB for the same.
- Run the migrations command
  ```python manage.py makemigrations```
  ```python manage.py migrate```
- Run the server: ```python manage.py runserver```
