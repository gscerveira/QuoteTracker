import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def get_owner(self):
        return self.user

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def get_owner(self):
        return self.project.get_owner()

    def __str__(self):
        return self.name


class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user = models.ForeignKey(User, related_name="stores", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("user", "name")

    def get_owner(self):
        return self.user

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"


class QuoteRequest(models.Model):
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
        return self.item.get_owner()

    def __str__(self):
        return f"Quote request for {self.item.name}"
