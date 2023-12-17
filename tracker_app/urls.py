from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ItemViewSet, QuoteRequestViewset


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'items', ItemViewSet)
router.register(r'quoterequests', QuoteRequestViewset)

urlpatterns = [
    path('', include(router.urls))
]
