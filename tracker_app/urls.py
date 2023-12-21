from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProjectViewSet, ItemViewSet, QuoteRequestViewset, UserRegistrationView, UserLoginView, UserLogoutView,
                    StoreViewset)


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'items', ItemViewSet)
router.register(r'quoterequests', QuoteRequestViewset)
router.register(r'stores', StoreViewset)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', include(router.urls))
]
