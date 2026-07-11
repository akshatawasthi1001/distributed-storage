# Distributed File Storage System

A production-ready backend application built with FastAPI that allows authenticated users to securely upload, manage, version, search, and download files. The project uses PostgreSQL for metadata storage and Docker for containerized deployment.

---

## Features

- User Registration & Login (JWT Authentication)
- Secure File Upload
- Download Files
- Delete Files
- File Metadata Management
- File Search
- File Versioning
- Pagination
- User-based File Ownership
- Dockerized Deployment
- PostgreSQL Integration

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- JWT Authentication
- Docker & Docker Compose
- Passlib (bcrypt)
- Uvicorn

---

## Project Structure

```
metadata-server/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── storage/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /auth/register | Register User |
| POST | /auth/login | Login |
| POST | /upload | Upload File |
| GET | /files | List Files |
| GET | /files/search | Search Files |
| GET | /files/{id} | File Metadata |
| GET | /download/{id} | Download File |
| PUT | /files/{id} | Replace File |
| DELETE | /files/{id} | Delete File |
| GET | /files/{id}/versions | Version History |
| GET | /files/{id}/versions/{version}/download | Download Specific Version |

---

## Authentication

The project uses JWT-based authentication.

Protected endpoints require:

Authorization: Bearer <access_token>

---

## Running the Project

Clone the repository

```bash
git clone https://github.com/akshatawasthi1001/distributed-storage.git
```

Navigate to the project

```bash
cd distributed-storage/metadata-server
```

Start Docker

```bash
docker compose up --build
```

Open Swagger UI

```
http://localhost:8000/docs
```

---

## Future Improvements

- AWS S3 Storage
- MinIO Integration
- Redis Caching
- Background Tasks using Celery
- File Sharing with Permissions
- Admin Dashboard

---

## Author

Akshat Awasthi
