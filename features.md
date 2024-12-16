<div align="center">
<h1>Project Architecture</h1>
</div>

# Context
- [Context](#context)
  - [Core Components](#core-components)
    - [Models](#models)
    - [Authentication](#authentication)
    - [API Endpoints](#api-endpoints)
    - [Documentation](#documentation)
  - [Key Features](#key-features)
  - [Technology Stack](#technology-stack)
  - [Workflow Example](#workflow-example)
  - [Security Considerations](#security-considerations)
  - [Development Setup](#development-setup)
  - [Postman/API Testing](#postmanapi-testing)

## Core Components

### Models

- **User:** Custom user model with email and date_joined
- **Project:** Represents a project with name, description, owner
- **ProjectMember:** Manages user roles in projects
- **Task:** Tracks project tasks with status, priority, assignment
- **Comment:** Allows commenting on tasks

[⬆️ Go to Context](#context)

### Authentication

- Uses JWT (JSON Web Token) authentication
- Endpoints for token obtain and refresh
- Supports multiple authentication methods:
  - JWT Authentication
  - Session Authentication
  - Basic Authentication

[⬆️ Go to Context](#context)

### API Endpoints

- **Users**
  - List/Create users
  - Retrieve/Update/Delete user details
- **Projects**
  - List/Create projects
  - Retrieve/Update/Delete project details
  - Manage project members
- **Tasks**
  - List tasks (can filter by project)
  - Create/Update/Delete tasks
  - Assign tasks to users
- **Comments**
  - Add comments to tasks
  - List/Update/Delete comments
- **Authentication**
  - `/api/token/`: Obtain JWT token
  - `/api/token/refresh/`: Refresh JWT token

[⬆️ Go to Context](#context)

### Documentation

- **Swagger UI:** Interactive API documentation
- **ReDoc:** Alternative documentation view
- **OpenAPI Schema** endpoint

[⬆️ Go to Context](#context)

## Key Features

- Role-based access control
- Project membership management
- Task tracking with status and priority
- Commenting system
- JWT-based authentication

[⬆️ Go to Context](#context)

## Technology Stack

- Django 5.1.4
- Django REST Framework
- drf-spectacular (OpenAPI documentation)
- Simple JWT (Authentication)
- SQLite (Development database)

[⬆️ Go to Context](#context)

## Workflow Example

1. Create a user
2. Obtain JWT token
3. Create a project
4. Add project members
5. Create tasks
6. Add comments to tasks

[⬆️ Go to Context](#context)

## Security Considerations

- JWT authentication
- Permissions control
- User-specific data access

[⬆️ Go to Context](#context)

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


## Running the Project

```bash
# In Terminal
python manage.py runserver
```

[⬆️ Go to Context](#context)

## Postman/API Testing

- Use JWT token for authenticated requests
- Endpoints available at `/api/`
- Swagger UI for interactive documentation

[⬆️ Go to Context](#context)
