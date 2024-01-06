from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProjectViewSet, ItemViewSet, QuoteRequestViewset, UserRegistrationView, UserLoginView, UserLogoutView,
                    StoreViewset)


router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'items', ItemViewSet, basename='items')
router.register(r'quoterequests', QuoteRequestViewset, basename='quoterequests')
router.register(r'stores', StoreViewset, basename='stores')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', include(router.urls))
]
