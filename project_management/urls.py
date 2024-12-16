from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# drf_spectacular imports
# from drf_spectacular.views import (
#     SpectacularAPIView, 
#     SpectacularRedocView, 
#     SpectacularSwaggerView
# )

# drf-yasg imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# views imports
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

# Configure drf-yasg schema view
schema_view = get_schema_view(
   openapi.Info(
      title="Project Management API",
      default_version='v1',
      description="A comprehensive API for managing projects, tasks, and team collaboration",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Home route
    path('', home_view, name='home'),
    
    # Admin site
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/', include((router.urls, 'api'), namespace='api')),
    
    # Custom user routes
    path('api/users/register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('api/users/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),

    # Authentication routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Swagger documentation routes
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Add drf-yasg routes
    path('api/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]