Certainly! Here's an updated version of the README.md file template that includes endpoints for token management and user operations:

```markdown
# FastAPI Bookstore API

This repository contains a FastAPI-based API for managing a bookstore inventory.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/fastapi-bookstore.git
   cd fastapi-bookstore
   ```

2. **Install dependencies using pip:**

   ```bash
   pip install -r requirements.txt
   ```

## Setting Up PostgreSQL Locally

1. **Install PostgreSQL:**
   - If you haven't already, download and install PostgreSQL from [PostgreSQL Downloads](https://www.postgresql.org/download/).

2. **Create Database and User:**
   - Open a PostgreSQL client (e.g., pgAdmin).
   - Create a new database and note down the database name.
   - Create a new user with a password and grant privileges to the database.

3. **Update `.env` File:**
   - Create a `.env` file in the root directory of the project with the following contents:

     ```dotenv
     SECRET_KEY=your_secret_key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     DATABASE_USER=your_db_user
     DATABASE_PASSWORD=your_db_password
     DATABASE=your_db_name
     ```

     Replace placeholders (`your_secret_key`, `your_db_user`, `your_db_password`, `your_db_name`) with your actual values.

## Running the FastAPI Server

Use the following command to start the FastAPI server with automatic reloading:

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## Endpoints

### Authentication

- **POST /token/**: Get an access token for authentication.
  - Request Body:
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - Response:
    ```json
    {
      "access_token": "your_access_token",
      "token_type": "bearer"
    }
    ```

### Users

- **POST /users/**: Create a new user.
  - Request Body:
    ```json
    {
      "username": "new_user",
      "password": "new_password"
    }
    ```
  - Response Model: User

### Books

- **GET /books/**: Retrieve a list of all books.
- **GET /books/{book_id}/**: Retrieve details of a specific book.
- **POST /books/**: Create a new book.
- **PUT /books/{book_id}/**: Update details of a specific book.
- **DELETE /books/{book_id}/**: Delete a specific book.

### Authors

- **GET /authors/**: Retrieve a list of all authors.
- **GET /authors/{author_id}/**: Retrieve details of a specific author.
- **POST /authors/**: Create a new author.
- **PUT /authors/{author_id}/**: Update details of a specific author.
- **DELETE /authors/{author_id}/**: Delete a specific author.

### Genres

- **GET /genres/**: Retrieve a list of all genres.
- **GET /genres/{genre_id}/**: Retrieve details of a specific genre.
- **POST /genres/**: Create a new genre.
- **PUT /genres/{genre_id}/**: Update details of a specific genre.
- **DELETE /genres/{genre_id}/**: Delete a specific genre.
```

This README provides comprehensive instructions for setting up the environment, running the FastAPI server, and accessing various API endpoints including authentication, user management, books, authors, and genres. Adjust the template according to your specific project needs and details.