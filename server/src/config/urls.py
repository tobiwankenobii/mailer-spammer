from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.emails.api.views import EmailConfigManagementViewSet
from apps.users.api.views import UserRegisterView

router = routers.DefaultRouter()
router.register(
    r"api/email-configs", EmailConfigManagementViewSet, basename="email_configs"
)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
]

api_patterns = [
    path(
        "api/users/register", UserRegisterView.as_view(), name="user_register"
    ),
]

urlpatterns += api_patterns
