from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vault(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PasswordEntry(TimeStampedModel):
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    password = models.TextField()  # Store encrypted password
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
