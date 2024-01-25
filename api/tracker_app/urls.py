from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.routers import DefaultRouter

from .views import (ItemViewSet, ProjectViewSet, StoreViewset, UserLoginView, UserLogoutView,
                    UserRegistrationView)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"items", ItemViewSet, basename="items")
router.register(r"stores", StoreViewset, basename="stores")

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

"""
URL patterns for the quotes tracker application.

This module defines the URL patterns for the quotes tracker application.
It includes the registration, login, and logout views, as well as the views
for managing projects, items, quote requests, and stores.

The URLs are defined using the Django `path` function and are mapped to the
corresponding view classes or functions.

The `router` object is used to automatically generate the URLs for all the
viewsets.

The `SpectacularAPIView`, `SpectacularSwaggerView`, and `SpectacularRedocView`
views are used to generate the API schema, Swagger UI, and ReDoc documentation
for the API.

Note: This module assumes that the necessary views and viewsets are imported
from the `.views` module.
"""
