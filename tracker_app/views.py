from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from .models import Project, Item, QuoteRequest
from .serializers import ProjectSerializer, ItemSerializer, QuoteRequestSerializer, UserSerializer
# Create your views here.


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('items', 'items__quoterequests')
    serializer_class = ProjectSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class QuoteRequestViewset(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
