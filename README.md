# Task Management REST API with Supabase Authentication

A production-ready, modular REST API built with **Python 3.10+**, **FastAPI**, **PostgreSQL / SQLite**, and **Supabase Auth**. Designed for the **FlyRank Backend Track (Week 4 Assignment — Authentication & Security)**.

---

## 🚀 Project Overview

This application extends the Task Management API with a secure authentication system powered by **Supabase Auth**. It implements JWT-based authentication, modular routers, a reusable authentication dependency, protected routes, interactive Swagger UI authorization, and repository-pattern database integration.

### Core Features

- **FastAPI Framework**: High performance, automatic payload validation via Pydantic v2, and OpenAPI schema generation.
- **Supabase Authentication**:
  - `POST /auth/signup`: User registration using Supabase Auth SDK.
  - `POST /auth/login`: User authentication returning JWT `access_token` and `refresh_token`.
  - `POST /auth/logout`: Protected user sign-out endpoint returning `204 No Content`.
- **Reusable Authentication Dependency**: `get_current_user` dependency in `app/dependencies.py` extracts Bearer tokens, verifies JWT signatures and expiry via Supabase, and injects the user into protected endpoints.
- **Public & Protected Endpoint Scoping**:
  - Public: `GET /`, `GET /health`, `GET /public/info`, `GET /tasks`, `GET /tasks/{id}`.
  - Protected: `GET /protected/profile`, `GET /protected/dashboard`, `POST /auth/logout`, `POST /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`.
- **Swagger UI Integration (`/docs`)**: Configured with `HTTPBearer` security scheme — displays lock icons 🔒 on protected routes and provides an interactive **Authorize** modal for testing Bearer tokens.
- **Database Repository Pattern**: Decoupled database architecture supporting both PostgreSQL (`psycopg2`) and SQLite.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Auth Provider**: Supabase Auth (`@supabase/supabase-js` / `supabase` Python SDK)
- **Database**: PostgreSQL (Docker container) / SQLite (`tasks.db`)
- **Environment Management**: `python-dotenv`
- **Documentation**: Swagger UI / OpenAPI 3.0 (`/docs`)

---

## 📁 Project Structure

```text
FlyRank_Intern/
├── app/
│   ├── __init__.py            # App package marker
│   ├── main.py                # FastAPI entry point & exception handlers
│   ├── models.py              # Pydantic schemas for Tasks
│   ├── auth_schemas.py        # Pydantic schemas for Auth (Signup, Login, User, Tokens)
│   ├── database.py            # SQLite database implementation & singleton export
│   ├── postgres_repository.py # PostgreSQL repository implementation
│   ├── supabase_client.py     # Singleton Supabase client initialized from environment
│   ├── dependencies.py        # Reusable get_current_user auth dependency & HTTPBearer scheme
│   └── routers/
│       ├── __init__.py        # Routers package marker
│       ├── auth.py            # Auth endpoints (/auth/signup, /auth/login, /auth/logout)
│       ├── public.py          # Public endpoints (/public/info)
│       └── protected.py       # Protected endpoints (/protected/profile, /protected/dashboard)
├── docs/                      # Screenshots & documentation assets
├── docker-compose.yml         # PostgreSQL Docker container configuration
├── init.sql                   # PostgreSQL initial database table schema
├── tasks.db                   # SQLite local database file (gitignored)
├── .env                       # Environment variables secret file (gitignored)
├── .env.example               # Environment variables public template
├── requirements.txt           # Python project dependencies
└── README.md                  # Complete project documentation
```

---

## 🔑 Environment Variables & Security

### Why `.env` MUST NEVER be Committed to Version Control

The `.env` file contains sensitive production credentials, API secrets, database passwords, and Supabase service keys (`SUPABASE_ANON_KEY`, `DATABASE_URL`). 

- **Security Risk**: Committing `.env` publicly allows unauthorized third parties to compromise your Supabase auth instance, modify your database, or steal user data.
- **Git Enforcement**: `.env` is explicitly listed in [.gitignore](file:///.gitignore). Only [.env.example](file:///.env.example) (containing safe placeholder names) is committed to git.

### Environment Schema

Create a local `.env` file at the project root using `.env.example` as a template:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=taskdb
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskdb

# Supabase Credentials
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

---

## ⚡ Supabase Setup Guide

1. **Create a Supabase Project**:
   - Navigate to [supabase.com](https://supabase.com) and create a new project.
2. **Disable Email Confirmation for Development**:
   - Go to **Authentication** → **Providers** → **Email**.
   - Turn **Confirm Email** to **OFF** so users can sign up and immediately sign in without email verification delays.
3. **Copy API Keys**:
   - Go to **Project Settings** → **API**.
   - Copy **Project URL** (e.g. `https://xxxx.supabase.co`) into `SUPABASE_URL`.
   - Copy **anon / public key** into `SUPABASE_ANON_KEY`.

---

## 💻 Installation & Running Locally

### 1. Clone the Repository
```bash
git clone <repository_url>
cd FlyRank_Intern
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Start Database (PostgreSQL via Docker)
```bash
docker compose up -d
```

### 4. Run FastAPI Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Server starts at: `http://localhost:8000`

---

## 📡 API Endpoints Reference Table

| Category | HTTP Verb | Path | Description | Required Auth | Success Code |
|---|---|---|---|---|---|
| **System** | `GET` | `/` | Root API metadata & endpoints | None | `200 OK` |
| **System** | `GET` | `/health` | Server health check | None | `200 OK` |
| **Auth** | `POST` | `/auth/signup` | Register new user account | None | `201 Created` |
| **Auth** | `POST` | `/auth/login` | Authenticate user & get JWT tokens | None | `200 OK` |
| **Auth** | `POST` | `/auth/logout` | Sign out current user session | Bearer JWT 🔒 | `204 No Content` |
| **Public** | `GET` | `/public/info` | Public informational message | None | `200 OK` |
| **Protected** | `GET` | `/protected/profile` | Authenticated user profile details | Bearer JWT 🔒 | `200 OK` |
| **Protected** | `GET` | `/protected/dashboard` | Authenticated user dashboard view | Bearer JWT 🔒 | `200 OK` |
| **Tasks** | `GET` | `/tasks` | List all tasks | None | `200 OK` |
| **Tasks** | `GET` | `/tasks/{id}` | Get single task by ID | None | `200 OK` |
| **Tasks** | `POST` | `/tasks` | Create a new task | None | `201 Created` |
| **Tasks** | `PUT` | `/tasks/{id}` | Update existing task | None | `200 OK` |
| **Tasks** | `DELETE` | `/tasks/{id}` | Delete task by ID | None | `204 No Content` |

---

## 🔒 How Authentication Works Under the Hood

```mermaid
sequenceDiagram
    participant Client as Client / Postman / Swagger
    participant FastAPI as FastAPI App
    participant Dep as get_current_user Dependency
    participant Supabase as Supabase Auth Service

    Client->>FastAPI: Request to Protected Route (Header: Authorization: Bearer <JWT>)
    FastAPI->>Dep: Invoke get_current_user()
    alt Header Missing or Invalid Format
        Dep-->>Client: 401 Unauthorized {"error": "Access token required"}
    else Header Present
        Dep->>Supabase: supabase.auth.get_user(token)
        alt Token Valid & Active
            Supabase-->>Dep: Returns User Object (id, email, created_at)
            Dep-->>FastAPI: Returns User Dict
            FastAPI-->>Client: 200 OK (Protected Data)
        else Token Expired or Invalid Signature
            Supabase-->>Dep: Throws Auth Error
            Dep-->>Client: 401 Unauthorized {"error": "Invalid or expired token"}
        end
    end
```

---

## 📖 Swagger UI Authorization (`/docs`)

FastAPI automatically generates interactive API documentation at:
`http://localhost:8000/docs`

### How to Authenticate in Swagger UI:
1. Execute `POST /auth/login` with your credentials and copy the `access_token`.
2. Click the green **Authorize 🔓** button at the top right of the Swagger UI.
3. Paste your `access_token` into the **Value** field.
4. Click **Authorize** and then **Close**.
5. All protected endpoints displaying the **Lock Icon 🔒** will now automatically pass your Bearer token!

---

## 🔒 Security Notes & Best Practices

1. **Bearer Token Transmission**: Always transmit tokens via `Authorization: Bearer <token>` HTTP headers, never via URL query parameters.
2. **Password Exposure**: Passwords are never returned in any response body or saved in plaintext.
3. **Pydantic Validation**: Payload inputs are strictly sanitized to prevent empty string injections or missing field crashes.
