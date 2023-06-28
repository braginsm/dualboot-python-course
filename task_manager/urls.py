"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from task_manager.main import views
from task_manager.main.admin import task_manager_admin_site
from task_manager.services.single_resource import BulkRouter

router = BulkRouter()
router.register(r"tags", views.TagViewSet, basename="tags")
router.register(r"current-user", views.CurrentUserViewSet, basename="current_user")

users = router.register(r"users", views.UserViewSet, basename="users")
users.register(
    r"tasks",
    views.UserTasksViewSet,
    basename="user_tasks",
    parents_query_lookups=["assigned_id"],
)

tasks = router.register(r"tasks", views.TaskViewSet, basename="tasks")
tasks.register(
    r"tags",
    views.TaskTagsViewSet,
    basename="task_tags",
    parents_query_lookups=["task_id"],
)

schema_view = get_schema_view(
    openapi.Info(
        title="Task manager API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="braginsm@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
