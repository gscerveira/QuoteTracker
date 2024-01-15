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
        description (TextField): The description of the item.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
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


class QuoteRequest(models.Model):
    """
    Represents a quote request in the system.

    Attributes:
        NEED_SEND (str): The status indicating that the request needs to be sent.
        SENT (str): The status indicating that the request has been sent.
        RECEIVED (str): The status indicating that a quote has been received.
        NEED_RESEND (str): The status indicating that the request needs to be resent.

        STATUS_CHOICES (list): The choices for the status field.

        id (UUIDField): The unique identifier for the quote request.
        item (ForeignKey): The item that the quote request is for.
        status (CharField): The status of the quote request.
        details (TextField): The details of the quote request.
        store (ForeignKey): The store that the quote request is sent to.
    """

    NEED_SEND = "need_to_send"
    SENT = "sent"
    RECEIVED = "received"
    NEED_RESEND = "need_to_resend"

    STATUS_CHOICES = [
        (NEED_SEND, "Need to Send Request"),
        (SENT, "Request Sent"),
        (RECEIVED, "Quote Received"),
        (NEED_RESEND, "Need to Resend Request"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(
        Item, related_name="quoterequests", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=NEED_SEND)
    details = models.TextField(blank=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="quoterequests"
    )

    def get_owner(self):
        """
        Gets the owner of the quote request.

        Returns:
            User: The user who owns the project that the item belongs to.
        """
        return self.item.get_owner()

    def __str__(self):
        """
        Get a string representation of the quote request.

        Returns:
            str: A string representation of the quote request.
        """
        return f"Quote request for {self.item.name}"
