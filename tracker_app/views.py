from rest_framework import viewsets
from .models import Project, Item, QuoteRequest
from .serializers import ProjectSerializer, ItemSerializer, QuoteRequestSerializer
# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('items', 'items__quoterequests')
    serializer_class = ProjectSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class QuoteRequestViewset(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
