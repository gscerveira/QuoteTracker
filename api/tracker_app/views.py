from django.contrib.auth import authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, views, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Item, Project, QuoteRequest, Store
from .serializers import (ItemSerializer, LoginSerializer, ProjectSerializer,
                          QuoteRequestSerializer, StoreSerializer,
                          UserSerializer)

# Create your views here.


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the object.

        Args:
            request (HttpRequest): The request object.
            view (View): The view object.
            obj (object): The object to check ownership for.

        Returns:
            bool: True if the user is the owner, False otherwise.
        """
        return obj.get_owner() == request.user


class UserRegistrationView(CreateAPIView):
    """
    View for user registration.

    Allows users to register by creating a new account.

    Serializer Class:
        UserSerializer

    HTTP Methods:
        POST: Create a new user account.

    Permissions:
        Allow any user (unauthenticated).
    """
    serializer_class = UserSerializer


class UserLoginView(views.APIView):
    """
    View for user login.

    Allows users to log in to their account.

    Serializer Class:
        LoginSerializer

    HTTP Methods:
        POST: Log in to the user account.

    Permissions:
        Allow any user (unauthenticated).
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            login(request, user)
            return Response({"detail": "Login successful."}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserLogoutView(views.APIView):
    """
    View for user logout.

    Allows users to log out of their account.

    HTTP Methods:
        POST: Log out of the user account.

    Permissions:
        Allow any authenticated user.
    """
    def post(self, request):
        logout(request)
        return Response(
            {"detail": "Logout successful"}, status=status.HTTP_204_NO_CONTENT
        )


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for projects.

    Allows users to perform CRUD operations on projects.

    Model:
        Project

    Serializer Class:
        ProjectSerializer

    HTTP Methods:
        GET: Retrieve a list of projects.
        POST: Create a new project.
        PUT: Update an existing project.
        PATCH: Partially update an existing project.
        DELETE: Delete an existing project.

    Permissions:
        Allow only authenticated users who are the owners of the projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for items.

    Allows users to perform CRUD operations on items.

    Model:
        Item

    Serializer Class:
        ItemSerializer

    HTTP Methods:
        GET: Retrieve a list of items.
        POST: Create a new item.
        PUT: Update an existing item.
        PATCH: Partially update an existing item.
        DELETE: Delete an existing item.

    Permissions:
        Allow only authenticated users who are the owners of the associated projects.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]


    def get_queryset(self):
        return Item.objects.filter(project__user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.validated_data.get("project")
        if project not in self.request.user.projects.all():
            raise PermissionDenied("Project doesn't exist")
        serializer.save()


class StoreViewset(viewsets.ModelViewSet):
    """
    ViewSet for stores.

    Allows users to perform CRUD operations on stores.

    Model:
        Store

    Serializer Class:
        StoreSerializer

    HTTP Methods:
        GET: Retrieve a list of stores.
        POST: Create a new store.
        PUT: Update an existing store.
        PATCH: Partially update an existing store.
        DELETE: Delete an existing store.

    Permissions:
        Allow only authenticated users who are the owners of the stores.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuoteRequestViewset(viewsets.ModelViewSet):
    """
    ViewSet for quote requests.

    Allows users to perform CRUD operations on quote requests.

    Model:
        QuoteRequest

    Serializer Class:
        QuoteRequestSerializer

    HTTP Methods:
        GET: Retrieve a list of quote requests.
        POST: Create a new quote request.
        PUT: Update an existing quote request.
        PATCH: Partially update an existing quote request.
        DELETE: Delete an existing quote request.

    Permissions:
        Allow only authenticated users who are the owners of the associated items.
    """
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["item"]

    def get_queryset(self):
        return QuoteRequest.objects.filter(item__project__user=self.request.user)

    def perform_create(self, serializer):
        item = serializer.validated_data.get("item")
        user_projects_items = Item.objects.filter(project__user=self.request.user)
        if item not in user_projects_items:
            raise PermissionDenied("Item doesn't exist")
        serializer.save()
