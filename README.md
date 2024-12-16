<div align="center">
<h1>Django Project Management API</h1>
</div>

# Context
- [Context](#context)
  - [Project Setup](#project-setup)
  - [Project Structure](#project-structure)
  - [Models Implementation](#models-implementation)
  - [Serializers](#serializers)
  - [Views and ViewSets](#views-and-viewsets)
  - [URLs Configuration](#urls-configuration)
  - [Settings Configuration](#settings-configuration)
  - [Final Step](#final-step)
  - [Home UI Setup](#home-ui-setup)

## Project Setup

1. **Create a Virtual Environment:**

    ```sh
    python -m venv venv
    ```

2. **Activate the Virtual Environment:**

    ```sh
    venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create the Django Project:**

    ```bash
    django-admin startproject project_management .
    ```

5. **Create a Django App:**

    ```bash
    python manage.py startapp core
    ```

[⬆️ Go to Context](#context)

## Project Structure

```txt
Django-Project-Management-API/
│
├── project_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── requirements.txt
└── manage.py
```

[⬆️ Go to Context](#context)

## Models Implementation

- In `core/models.py`, implement the Django models for the Project and Task models.

    ```py
    from django.db import models
    from django.contrib.auth.models import AbstractUser
    from django.utils.translation import gettext_lazy as _

    class User(AbstractUser):
        """
        Custom User model extending Django's AbstractUser
        Adds additional fields like first_name, last_name
        """
        email = models.EmailField(_('email address'), unique=True)
        date_joined = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.username

    class Project(models.Model):
        """
        Represents a project in the management system
        """
        name = models.CharField(max_length=200)
        description = models.TextField(blank=True)
        owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name

    class ProjectMember(models.Model):
        """
        Represents project membership and roles
        """
        ROLE_CHOICES = [
            ('admin', 'Admin'),
            ('member', 'Member')
        ]
        project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

        class Meta:
            unique_together = ('project', 'user')

    class Task(models.Model):
        """
        Represents tasks within a project
        """
        STATUS_CHOICES = [
            ('todo', 'To Do'),
            ('in_progress', 'In Progress'),
            ('done', 'Done')
        ]
        PRIORITY_CHOICES = [
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ]

        title = models.CharField(max_length=200)
        description = models.TextField(blank=True)
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
        priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
        project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
        assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        due_date = models.DateTimeField(null=True, blank=True)

        def __str__(self):
            return self.title

    class Comment(models.Model):
        """
        Represents comments on tasks
        """
        content = models.TextField()
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Comment by {self.user.username} on {self.task.title}"
    ```

[⬆️ Go to Context](#context)

## Serializers

- In `core/serializers.py`, implement the Django serializers for the Project and Task models.

    ```py
    from rest_framework import serializers
    from .models import User, Project, ProjectMember, Task, Comment

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
            read_only_fields = ['id', 'date_joined']

    class ProjectSerializer(serializers.ModelSerializer):
        owner = UserSerializer(read_only=True)

        class Meta:
            model = Project
            fields = ['id', 'name', 'description', 'owner', 'created_at']
            read_only_fields = ['id', 'created_at']

    class ProjectMemberSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)

        class Meta:
            model = ProjectMember
            fields = ['id', 'project', 'user', 'role']

    class TaskSerializer(serializers.ModelSerializer):
        assigned_to = UserSerializer(read_only=True)
        project = ProjectSerializer(read_only=True)

        class Meta:
            model = Task
            fields = ['id', 'title', 'description', 'status', 'priority', 
                    'project', 'assigned_to', 'created_at', 'due_date']
            read_only_fields = ['id', 'created_at']

    class CommentSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)

        class Meta:
            model = Comment
            fields = ['id', 'content', 'user', 'task', 'created_at']
            read_only_fields = ['id', 'created_at']
    ```

[⬆️ Go to Context](#context)

## Views and ViewSets

- In `core/views.py`, implement the Django views for the Project and Task models.

    ```py
    from rest_framework import viewsets, permissions
    from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
    from .models import User, Project, ProjectMember, Task, Comment
    from .serializers import (
        UserSerializer, ProjectSerializer, 
        ProjectMemberSerializer, TaskSerializer, CommentSerializer
    )

    class UserViewSet(viewsets.ModelViewSet):
        """
        API endpoint for managing users
        """
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [permissions.IsAuthenticated]

        @extend_schema(
            description="List all users",
            responses={200: UserSerializer(many=True)}
        )
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)

    class ProjectViewSet(viewsets.ModelViewSet):
        """
        API endpoint for managing projects
        """
        queryset = Project.objects.all()
        serializer_class = ProjectSerializer
        permission_classes = [permissions.IsAuthenticated]

        def perform_create(self, serializer):
            serializer.save(owner=self.request.user)

        @extend_schema(
            description="List all projects",
            responses={200: ProjectSerializer(many=True)}
        )
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)

    class ProjectMemberViewSet(viewsets.ModelViewSet):
        """
        API endpoint for managing project members
        """
        queryset = ProjectMember.objects.all()
        serializer_class = ProjectMemberSerializer
        permission_classes = [permissions.IsAuthenticated]

    class TaskViewSet(viewsets.ModelViewSet):
        """
        API endpoint for managing tasks
        """
        queryset = Task.objects.all()
        serializer_class = TaskSerializer
        permission_classes = [permissions.IsAuthenticated]

        @extend_schema(
            description="List tasks",
            parameters=[
                OpenApiParameter(
                    name='project_id', 
                    type=OpenApiTypes.INT, 
                    location=OpenApiParameter.QUERY,
                    description="Filter tasks by project ID"
                )
            ],
            responses={200: TaskSerializer(many=True)}
        )
        def list(self, request, *args, **kwargs):
            project_id = request.query_params.get('project_id')
            if project_id:
                self.queryset = self.queryset.filter(project_id=project_id)
            return super().list(request, *args, **kwargs)

    class CommentViewSet(viewsets.ModelViewSet):
        """
        API endpoint for managing comments
        """
        queryset = Comment.objects.all()
        serializer_class = CommentSerializer
        permission_classes = [permissions.IsAuthenticated]

        @extend_schema(
            description="List comments",
            parameters=[
                OpenApiParameter(
                    name='task_id', 
                    type=OpenApiTypes.INT, 
                    location=OpenApiParameter.QUERY,
                    description="Filter comments by task ID"
                )
            ],
            responses={200: CommentSerializer(many=True)}
        )
        def list(self, request, *args, **kwargs):
            task_id = request.query_params.get('task_id')
            if task_id:
                self.queryset = self.queryset.filter(task_id=task_id)
            return super().list(request, *args, **kwargs)
    ```

[⬆️ Go to Context](#context)

## URLs Configuration

- In `core/urls.py`, define the URL patterns for the Project and Task models.

    ```py
    from django.contrib import admin
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )
    from drf_spectacular.views import (
        SpectacularAPIView, 
        SpectacularRedocView, 
        SpectacularSwaggerView
    )

    from core.views import (
        UserViewSet, ProjectViewSet, 
        ProjectMemberViewSet, TaskViewSet, CommentViewSet
    )

    router = DefaultRouter()
    router.register(r'users', UserViewSet)
    router.register(r'projects', ProjectViewSet)
    router.register(r'project-members', ProjectMemberViewSet)
    router.register(r'tasks', TaskViewSet)
    router.register(r'comments', CommentViewSet)

    urlpatterns = [
        # Admin site
        path('admin/', admin.site.urls),
        
        # API routes
        path('api/', include(router.urls)),
        
        # Authentication routes
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
        # Swagger documentation routes
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
    ```

[⬆️ Go to Context](#context)

## Settings Configuration

- In `project_management/settings.py`, configure the Django settings for the Project and Task models.

    ```py
    # Add to INSTALLED_APPS
    INSTALLED_APPS = [
        ...
        'rest_framework',
        'rest_framework_simplejwt',
        'core',
    ]

    # Authentication
    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }
    
    # Spectacular Settings
    SPECTACULAR_SETTINGS = {
        'TITLE': 'Project Management API',
        'DESCRIPTION': 'A comprehensive API for managing projects, tasks, and team collaboration',
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': True,
        'COMPONENT_SPLIT_REQUEST': True,
        'SWAGGER_UI_SETTINGS': {
            'deepLinking': True,
            'persistAuthorization': True,
        },
    }

    # Custom User Model
    AUTH_USER_MODEL = 'core.User'
    ```

[⬆️ Go to Context](#context)

## Final Step

- Migrate and run the project

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```

[⬆️ Go to Context](#context)

## Home UI Setup

- Create a base template in `core/templates/base.html`

    ```jinja
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Project Management API</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body { 
                background-color: #f4f6f9; 
                font-family: 'Arial', sans-serif;
            }
            .jumbotron { 
                background-color: #ffffff; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
            }
            .card { 
                transition: transform 0.3s; 
                margin-bottom: 20px;
            }
            .card:hover { 
                transform: scale(1.03); 
                box-shadow: 0 10px 20px rgba(0,0,0,0.12);
            }
            .list-group-item a {
                color: #007bff;
                text-decoration: none;
            }
            .list-group-item a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
            <a class="navbar-brand" href="{% url 'home' %}">Project Management API</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'swagger-ui' %}">Swagger UI</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'redoc' %}">ReDoc</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'token_obtain_pair' %}">Get Token</a>
                    </li>
                </ul>
            </div>
        </nav>

        {% block content %}{% endblock %}
        
        <footer class="footer mt-auto py-3 bg-light text-center">
            <div class="container">
                <span class="text-muted">© 2024 Project Management API. All rights reserved.</span>
            </div>
        </footer>

        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    ```

- Create a home template in `core/templates/home.html`

    ```jinja
    {% extends 'base.html' %}

    {% block content %}
    <div class="container mt-5">
        <div class="jumbotron text-center">
            <h1 class="display-4">{{ title }}</h1>
            <p class="lead">{{ description }}</p>
            <hr class="my-4">
            <p>Explore our API endpoints and manage your projects efficiently.</p>
        </div>

        <div class="row">
            {% for route in api_routes %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        <h5 class="card-title mb-0">{{ route.name }}</h5>
                    </div>
                    <div class="card-body">
                        <p class="card-text">{{ route.description }}</p>
                        <ul class="list-group list-group-flush">
                            {% for endpoint in route.endpoints %}
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span class="badge badge-primary mr-2">{{ endpoint.method }}</span>
                                {{ endpoint.path }}
                                <small class="text-muted">{{ endpoint.description }}</small>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5 class="card-title mb-0">Quick Links</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4">
                                <h6>API Routes</h6>
                                <ul class="list-unstyled">
                                    <li><a href="{% url 'api:user-list' %}" class="btn btn-outline-primary btn-sm mb-2">Users API</a></li>
                                    <li><a href="{% url 'api:project-list' %}" class="btn btn-outline-primary btn-sm mb-2">Projects API</a></li>
                                    <li><a href="{% url 'api:task-list' %}" class="btn btn-outline-primary btn-sm mb-2">Tasks API</a></li>
                                </ul>
                            </div>
                            <div class="col-md-4">
                                <h6>Authentication</h6>
                                <ul class="list-unstyled">
                                    <li><a href="{% url 'token_obtain_pair' %}" class="btn btn-outline-primary btn-sm mb-2">Obtain Token</a></li>
                                    <li><a href="{% url 'token_refresh' %}" class="btn btn-outline-primary btn-sm mb-2">Refresh Token</a></li>
                                </ul>
                            </div>
                            <div class="col-md-4">
                                <h6>Documentation</h6>
                                <ul class="list-unstyled">
                                    <li><a href="{% url 'swagger-ui' %}" class="btn btn-outline-info btn-sm mb-2">Swagger UI</a></li>
                                    <li><a href="{% url 'redoc' %}" class="btn btn-outline-info btn-sm mb-2">ReDoc</a></li>
                                    <li><a href="{% url 'schema' %}" class="btn btn-outline-info btn-sm mb-2">OpenAPI Schema</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    ```

- Create a home view in `core/views.py`

    ```py
    def home_view(request):
        """
        Home page view that provides an overview of the Project Management API
        """
        api_routes = [
            {
                'name': 'Users',
                'description': 'Manage user accounts',
                'endpoints': [
                    {'method': 'GET', 'path': '/api/users/', 'description': 'List all users'},
                    {'method': 'POST', 'path': '/api/users/', 'description': 'Create a new user'},
                ]
            },
            {
                'name': 'Projects',
                'description': 'Manage project details',
                'endpoints': [
                    {'method': 'GET', 'path': '/api/projects/', 'description': 'List all projects'},
                    {'method': 'POST', 'path': '/api/projects/', 'description': 'Create a new project'},
                ]
            },
            {
                'name': 'Tasks',
                'description': 'Manage project tasks',
                'endpoints': [
                    {'method': 'GET', 'path': '/api/tasks/', 'description': 'List all tasks'},
                    {'method': 'POST', 'path': '/api/tasks/', 'description': 'Create a new task'},
                ]
            },
            {
                'name': 'Authentication',
                'description': 'JWT Token Management',
                'endpoints': [
                    {'method': 'POST', 'path': '/api/token/', 'description': 'Obtain JWT token'},
                    {'method': 'POST', 'path': '/api/token/refresh/', 'description': 'Refresh JWT token'},
                ]
            },
            {
                'name': 'Documentation',
                'description': 'API Documentation',
                'endpoints': [
                    {'method': 'GET', 'path': '/api/docs/', 'description': 'Swagger UI'},
                    {'method': 'GET', 'path': '/api/redoc/', 'description': 'ReDoc Documentation'},
                    {'method': 'GET', 'path': '/api/schema/', 'description': 'OpenAPI Schema'},
                ]
            }
        ]
        
        context = {
            'title': 'Project Management API',
            'description': 'A comprehensive API for managing projects, tasks, and team collaboration',
            'api_routes': api_routes
        }
        return render(request, 'home.html', context)
    ```

- Update home URL pattern in `core/urls.py`

    ```py
    from django.contrib import admin
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )
    from drf_spectacular.views import (
        SpectacularAPIView, 
        SpectacularRedocView, 
        SpectacularSwaggerView
    )

    from core.views import (
        UserViewSet, ProjectViewSet, 
        ProjectMemberViewSet, TaskViewSet, CommentViewSet,
        home_view
    )

    router = DefaultRouter()
    router.register(r'users', UserViewSet)
    router.register(r'projects', ProjectViewSet)
    router.register(r'project-members', ProjectMemberViewSet)
    router.register(r'tasks', TaskViewSet)
    router.register(r'comments', CommentViewSet)

    urlpatterns = [
        # Home route
        path('', home_view, name='home'),
        
        # Admin site
        path('admin/', admin.site.urls),
        
        # API routes
        path('api/', include((router.urls, 'api'), namespace='api')),
        
        # Authentication routes
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
        # Swagger documentation routes
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
    ```

[⬆️ Go to Context](#context)
