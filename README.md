# Hackathon Project Management Platform

A full-stack project management platform built for hackathons, allowing users to create, manage, and discover projects with authentication and user accounts.

## 🚀 Features

- **User Authentication**: Sign up and login with secure password hashing (Argon2)
- **Project Management**: Create, view, and manage hackathon projects
- **User Accounts**: Manage user profiles and project ownership
- **Session Management**: Persistent session tracking
- **Responsive UI**: Modern Next.js frontend with Tailwind CSS

## 📋 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with asyncpg
- **Authentication**: Argon2-cffi for password hashing
- **CORS**: Middleware for cross-origin requests

### Frontend
- **Framework**: Next.js 16+ with TypeScript
- **Styling**: Pollen CSS + UnoCSS with Tailwind
- **Form Handling**: Formik + Yup validation
- **Markdown Support**: Marked.js for rendering

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database Migrations**: SQL migrations with versioning
- **Development**: Mise.toml for environment management

## 📁 Project Structure

```
├── api/              # FastAPI backend
│   ├── app/
│   │   ├── main.py   # API entry point
│   │   ├── auth.py   # Authentication routes
│   │   ├── projects.py  # Project routes
│   │   ├── db.py     # Database connection
│   │   └── deps.py   # Dependency injection
│   └── pyproject.toml
├── nextjs/           # Next.js frontend
│   ├── app/          # App router pages
│   ├── components/   # React components
│   └── lib/          # Utilities
├── db/               # Database setup
│   ├── migrations/   # SQL migrations
│   └── Dockerfile
└── docker-compose.yml
```

## 🛠️ Setup & Installation

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.14+ (for local backend development)

### Quick Start with Docker

```bash
docker-compose up
```

This will start:
- **API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Database**: PostgreSQL on port 5432

### Local Development Setup

#### Backend
```bash
cd api
uv sync  # Install dependencies with uv package manager
uv run fastapi run app/main.py  # Start dev server
```

#### Frontend
```bash
cd nextjs
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

## 📚 API Endpoints

### Authentication Routes (`/auth`)
- `POST /auth/register` - Create new user account
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Projects Routes (`/projects`)
- `GET /projects` - List all projects
- `GET /projects/{id}` - Get project details
- `POST /projects` - Create new project
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

## 🗄️ Database Schema

### Users Table
- `id` (UUID, PK)
- `name` (VARCHAR)
- `password` (VARCHAR, hashed)
- `is_admin` (BOOLEAN)
- `email` (VARCHAR, unique)
- `created_at` (TIMESTAMPTZ)

### Projects Table
- `id` (UUID, PK)
- `name` (TEXT)
- `description` (TEXT)
- `github_url` (TEXT, optional)
- `owner_user_id` (UUID, FK → users)
- `created_at` (TIMESTAMPTZ)

### Sessions Table
- `id` (UUID, PK)
- `user_id` (UUID, FK → users)
- `token` (TEXT)
- `created_at` (TIMESTAMPTZ)

## 🔐 Environment Variables

Create a `.env` file or configure via docker-compose overrides:

```env
CORS_ALLOWED_ORIGIN=http://localhost:3000
DATABASE_URL=postgresql://user:password@db:5432/hackathon
```

## 📦 Available Commands

### API
- `uv sync` - Install dependencies
- `ruff check/format` - Linting and formatting

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Check code with Biome
- `npm run format` - Format code with Biome
- `npm run pollen` - Generate CSS from Pollen

## 🐳 Docker Compose Services

- **api**: FastAPI backend on port 8000
- **nextjs**: Next.js frontend on port 3000
- **db**: PostgreSQL database on port 5432

## 📝 Development Notes

- Frontend uses TypeScript with strict type checking
- Backend uses async/await patterns for non-blocking I/O
- Database migrations are version-controlled in SQL
- CSS uses Pollen + UnoCSS for utility-first styling

## 📄 License

Hackathon Project
