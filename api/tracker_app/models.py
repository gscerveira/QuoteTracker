import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """
    Custom user model.

    Attributes:
        id (UUIDField): The unique identifier for the user.
    """ 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Project(models.Model):
    """
    Represents a project in the system.

    Attributes:
        id (UUIDField): The unique identifier for the project.
        user (ForeignKey): The user who owns the project.
        name (CharField): The name of the project.
        description (TextField): The description of the project.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def get_owner(self):
        """
        Gets the owner of the project.

        Returns:
            User: The user who owns the project.
        """
        return self.user

    def __str__(self):
        """
        Get a string representation of the project.

        Returns:
            str: The name of the project.
        """
        return self.name


class Item(models.Model):
    """
    Represents an item in the system.

    Attributes:
        id (UUIDField): The unique identifier for the item.
        project (ForeignKey): The project that the item belongs to.
        name (CharField): The name of the item.
        status (CharField): The status of the item.
        description (TextField): The description of the item.
    """

    NEED_SEND = "need_to_send"
    SENT = "sent"
    RECEIVED = "received"
    NEED_RESEND = "need_to_resend"
    DONE = "done"

    STATUS_CHOICES = [
        (NEED_SEND, "Need to Send Request"),
        (SENT, "Request Sent"),
        (RECEIVED, "Quote Received"),
        (NEED_RESEND, "Need to Resend Request"),
        (DONE, "Done"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=NEED_SEND)
    store = models.ForeignKey("Store", related_name="items", on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def get_owner(self):
        """
        Gets the owner of the item.

        Returns:
            User: The user who owns the project that the item belongs to.
        """
        return self.project.get_owner()

    def __str__(self):
        """
        Get a string representation of the item.

        Returns:
            str: The name of the item.
        """
        return self.name


class Store(models.Model):
    """
    Represents a store in the system.

    Attributes:
        id (UUIDField): The unique identifier for the store.
        user (ForeignKey): The user who created the store.
        name (CharField): The name of the store.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="stores", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("user", "name")

    def get_owner(self):
        """
        Gets the owner of the store.

        Returns:
            User: The user who owns the store.
        """
        return self.user

    def __str__(self):
        """
        Get a string representation of the store.

        Returns:
            str: The name of the store and the username of the owner.
        """
        return f"{self.name} (User: {self.user.username})"
