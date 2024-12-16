from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import User, Project, ProjectMember, Task, Comment
from .serializers import (
    UserSerializer, ProjectSerializer, 
    ProjectMemberSerializer, TaskSerializer, CommentSerializer
)
from django.shortcuts import render

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