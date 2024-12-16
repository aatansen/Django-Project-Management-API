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
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        required=True  # Make user required
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), 
        required=True  # Make project required
    )

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role']
        read_only_fields = ['id']

    def validate(self, data):
        """
        Validation to prevent duplicate project memberships during creation
        Allow role updates for existing memberships
        """
        # Check if this is an update operation
        instance = getattr(self, 'instance', None)
        
        # If this is an update and the instance exists, allow the update
        if instance is not None:
            return data
        
        # For new memberships, check for existing membership
        existing_membership = ProjectMember.objects.filter(
            project=data['project'], 
            user=data['user']
        ).exists()
        
        if existing_membership:
            raise serializers.ValidationError("User is already a member of this project.")
        
        return data

    def create(self, validated_data):
        """
        Custom create method to handle project member creation
        """
        # Ensure both project and user are provided
        if 'project' not in validated_data or 'user' not in validated_data:
            raise serializers.ValidationError("Both project and user must be specified when creating a project member.")
        
        return ProjectMember.objects.create(**validated_data)

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), 
        required=True  # Make project required
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 
                  'project', 'assigned_to', 'created_at', 'due_date']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """
        Custom create method to handle task creation with project
        """
        # Ensure project is provided
        if 'project' not in validated_data:
            raise serializers.ValidationError("A project must be specified when creating a task.")
        
        return Task.objects.create(**validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), 
        required=True  # Make task required
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        """
        Custom create method to handle comment creation with task
        """
        # Ensure task is provided
        if 'task' not in validated_data:
            raise serializers.ValidationError("A task must be specified when creating a comment.")
        
        return Comment.objects.create(**validated_data)