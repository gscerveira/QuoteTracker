from rest_framework import viewsets, status, views
from rest_framework.response import Response
from .models import Project, Item, QuoteRequest
from .serializers import ProjectSerializer, ItemSerializer, QuoteRequestSerializer, UserSerializer
# Create your views here.


class UserRegistrationView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('items', 'items__quoterequests')
    serializer_class = ProjectSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class QuoteRequestViewset(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
