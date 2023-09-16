# FastAPI CRUD API

This repository contains a CRUD (Create, Read, Update and Delete) API developed with FastAPI, a modern Python framework for creating APIs quickly and easily. This API provides endpoints to manage a collection of users, allowing the basic operations of a CRUD system on them.

## Key features

- Fast and efficient**: FastAPI is known for its high performance and low resource consumption, making it ideal for applications that require a high workload.
- Automatic validation**: FastAPI uses Pydantic to automatically validate incoming requests and outgoing responses, ensuring data integrity.
- Interactive documentation**: FastAPI automatically generates interactive API documentation, making it easy for developers to understand how to use it.
- Full CRUD method support**: The API includes endpoints for creating, reading, updating and deleting users, following CRUD best practices.

## Basic use

1. **Clone the repository**:https://github.com/JuanMartinGallo/MongoDB-Fastapi-REST-API-CRUD.git


2. **Install the dependencies**:pip install -r requirements.txt


3. **Run the application**:uvicorn app:app --reload


4. **Explore the documentation**:

Open a browser and navigate to `http://localhost:8000/docs` to access the interactive API documentation.

## Available endpoints

- GET /users : Gets the list of users.
- GET /users/{id} : Gets an user by its ID.
- POST /users : Creates a new user.
- PUT /users/{id} : Updates an existing user.
- DELETE /users/{id} : Deletes an user by its ID.
- POST /login : Login an excisting user
- POST /post-image : returns information about the uploaded image

## Contributions

Contributions are welcome! If you want to improve this CRUD API, feel free to submit a pull request. Make sure to follow the project contribution guidelines.
