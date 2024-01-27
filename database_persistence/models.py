from django.conf import settings
from django.db import models


class TrackableModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="created_%(class)s",
        on_delete=models.SET_NULL,
        default=None,
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="modified_%(class)s",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        abstract = True
