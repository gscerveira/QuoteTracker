from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate, login, logout
from .models import Project, Item, QuoteRequest
from .serializers import ProjectSerializer, ItemSerializer, QuoteRequestSerializer, UserSerializer
# Create your views here.


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(views.APIView):
    def post(self, request):
        user = authenticate(request, **request.data)
        if user:
            login(request, user)
            return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('items', 'items__quoterequests')
    serializer_class = ProjectSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class QuoteRequestViewset(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
