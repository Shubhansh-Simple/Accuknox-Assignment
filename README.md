
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

## Authentication

  Accuknox-Assignment API uses JWT token-based authentication. To authenticate requests, include an `Authorization` header in the following format:

  ```
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```

### API Endpoints 
<b>NoTE</b> : Requests must include <i><b>strict forward slashes</b></i> at the end for proper routing


### User Endpoints

| HTTP Method | Authentication | Endpoint | Description |
| --- | --- | --- | --- |
| POST | No | /users/signup/  | Register a new user |
| POST | No | /users/login/   | Authenticate user and return a JWT token |
| GET | Yes | /users/  | Return list of users with pagination of 10 records |
| GET | Yes | /users/?q='jai'  | Search users by firstname or lastname. Partial matches are supported |
| GET | Yes | /users/?q='some@gmail.com'  | Search users by exact email address |

### Friends Endpoints

| HTTP Method | Authentication | Endpoint | Description |
| --- | --- | --- | --- |
| GET | Yes | /friends/ | Retrieve a list of your friends |
| GET | Yes | /friends/request-pending-list/ | Retrieve a list of pending friend requests recieved. |
| POST | Yes | /friends/request-sent/7/ | Sent friend request to user with ID 7 |
| POST | Yes | /friends/request-accept/1/ | Accept a friend request with ID 1 |
| POST | Yes | /friends/request-reject/1/ | Reject a friend request with ID 1 |



