from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from dispatches.views import VerifyClaimView
from config.health import health, readiness

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", health),
    path("readyz/", readiness),
    path("api/auth/token/", TokenObtainPairView.as_view()),
    path("api/auth/token/refresh/", TokenRefreshView.as_view()),
    path("api/accounts/", include("accounts.urls")),
    path("api/incidents/", include("incidents.urls")),
    path("api/dispatches/", include("dispatches.urls")),
    path("api/etc/", include("etc_claims.urls")),
    path("verify/claim/", VerifyClaimView.as_view()),
]
