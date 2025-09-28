# Backend: Simple Movie App (FastAPI)

This is the backend service for the ReactJS Movie App, built with **FastAPI**. It provides REST API endpoints for managing users and their favorite movies.

---

## Setup

### Prepare virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run server

For development with hot reload:

```bash
uvicorn main:app --reload
```

The API docs will be available at:

- Swagger UI: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Hello Endpoint

| Method | URL      | Description                  | Params | Request Body | Response                 |
| :----- | :------- | :--------------------------- | :----- | :----------- | :----------------------- |
| GET    | `/hello` | Test route for server health | None   | None         | `{ "message": "Hello" }` |

---

### User Endpoints

| Method | URL      | Description    | Params | Request Body                               | Response                                                                  |
| :----- | :------- | :------------- | :----- | :----------------------------------------- | :------------------------------------------------------------------------ |
| GET    | `/user/` | Get all users  | None   | None                                       | List of users with `user_id`, `username`, `password`, and their favorites |
| POST   | `/user/` | Add a new user | None   | `{ "username": "str", "password": "str" }` | Created user object                                                       |

---

### Favorites Endpoints

| Method | URL           | Description                    | Params                    | Request Body                                                                                      | Response                                   |
| :----- | :------------ | :----------------------------- | :------------------------ | :------------------------------------------------------------------------------------------------ | :----------------------------------------- |
| GET    | `/favorites/` | Get favorite movies for a user | `user_id: int` (required) | None                                                                                              | List of favorite movies with movie details |
| POST   | `/favorites/` | Add a new favorite movie       | None                      | `{ "user_id": int, "movie_id": int, "movie_name": "str", "movie_description": "str (optional)" }` | Created favorite entry                     |

---

## Data Models

### User

```json
{
  "user_id": 1,
  "username": "john",
  "password": "hashed",
  "favorites": []
}
```

### Favorite

```json
{
  "user_id": 1,
  "movie_id": 101,
  "movie_name": "Inception",
  "movie_description": "A mind-bending thriller"
}
```

---
