from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from .models import Project, Item, QuoteRequest, Store
from .serializers import (ProjectSerializer, ItemSerializer, QuoteRequestSerializer, UserSerializer, LoginSerializer,
                          StoreSerializer)
# Create your views here.


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            login(request, user)
            return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        if project not in self.request.user.projects.all():
            raise PermissionDenied("Project doesn't exist")
        serializer.save()


class StoreViewset(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuoteRequestViewset(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        item = serializer.validated_data.get('item')
        user_projects_items = Item.objects.filter(project__user=self.request.user)
        if item not in user_projects_items:
            raise PermissionDenied("Item doesn't exist")
        serializer.save()
