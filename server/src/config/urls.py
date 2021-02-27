from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api.views import UserRegisterView

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
]

api_patterns = [
    path(
        "api/users/register", UserRegisterView.as_view(), name="user_register"
    ),
]

urlpatterns += api_patterns
