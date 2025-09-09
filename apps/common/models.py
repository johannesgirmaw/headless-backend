"""
Base models for the headless SaaS platform.
Provides common functionality like soft delete, timestamps, and audit fields.
"""

from django.db import models
from django.utils import timezone
import uuid


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted objects by default."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """
    Abstract base model that provides soft delete functionality.
    Objects are not actually deleted from the database, but marked as deleted.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )

    # Managers
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Includes soft-deleted objects

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self, user=None):
        """Soft delete this instance."""
        self.deleted_at = timezone.now()
        if user:
            self.updated_by = user
        self.save(update_fields=['deleted_at', 'updated_by'])

    def restore(self, user=None):
        """Restore this soft-deleted instance."""
        self.deleted_at = None
        if user:
            self.updated_by = user
        self.save(update_fields=['deleted_at', 'updated_by'])

    @property
    def is_deleted(self):
        """Check if this instance is soft-deleted."""
        return self.deleted_at is not None


class TimestampedModel(models.Model):
    """
    Abstract base model that provides timestamp fields.
    Used for models that don't need soft delete functionality.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class BaseModel(SoftDeleteModel):
    """
    Base model that combines soft delete with additional common fields.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
