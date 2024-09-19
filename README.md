
# Accuknox-Assignment

## Let's get started
This is a social media application (Backend) built with Django & Django Rest Framework


### Features/Functionalities
- Create User
- User Authorization
- Add Friends
- View Friends
- Search for Users


## Instructions to Dockerize the Django Application

This README provides a step-by-step guide on how to build and run a Dockerized Django application

### Prerequisities
Ensure you have the following installed on your system:
- Docker
- Docker Compose


### Building and Running the Application
- **Clone the repository (if you haven't already):** 
  ```sh
  git clone https://github.com/Shubhansh-Simple/Accuknox-Assignment.git
  cd Accuknox-Assignment
  ```

- **Create a .env file in root directory of the project with the following configuration:**
  ```sh
  DEBUG=True
  SECRET_KEY='your-secret-key-here'
  ```

- **Build and start the application:**
  ```sh
  docker compose up --build
  ```
  This command will build the Docker image as specified in the `Dockerfile` and `docker-compose.yml` file and start the application in a container.

- **Apply migrations & create superuser**

  - Stop the running container using Ctrl+C
  - Run migrations to set up the database:

  ```sh
  docker compose run web python manage.py migrate                # Apply Migrations
  ```
  - Create a superuser for accessing the Django admin panel
  ```sh
  docker compose run web python manage.py createsuperuser        # To create a superuser
  ```

- **Restart the Application**
After applying the migrations, restart the container to run the application

  ```sh
  docker compose up
  ```
  This application will be accessible at:
  ```sh
  http://localhost:8000/
  ```

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
  ```sh
  python manage.py makemigrations
  ```
  ```sh
  python manage.py migrate
  ```
- Run the server: ```python manage.py runserver```
