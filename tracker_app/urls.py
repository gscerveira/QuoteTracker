from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProjectViewSet, ItemViewSet, QuoteRequestViewset, UserRegistrationView, UserLoginView, UserLogoutView,
                    StoreViewset)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'items', ItemViewSet, basename='items')
router.register(r'quoterequests', QuoteRequestViewset, basename='quoterequests')
router.register(r'stores', StoreViewset, basename='stores')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
