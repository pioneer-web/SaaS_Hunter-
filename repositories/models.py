import uuid
from django.db import models

class Repository(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    github_id = models.BigIntegerField(unique=True)
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=520, unique=True)
    url = models.URLField(max_length=1000)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=120, blank=True)
    topics = models.JSONField(default=list, blank=True)
    stars = models.PositiveIntegerField(default=0)
    forks = models.PositiveIntegerField(default=0)
    watchers = models.PositiveIntegerField(default=0)
    open_issues = models.PositiveIntegerField(default=0)
    license_spdx = models.CharField(max_length=80, blank=True)
    is_fork = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created_at_github = models.DateTimeField(null=True, blank=True)
    updated_at_github = models.DateTimeField(null=True, blank=True)
    pushed_at_github = models.DateTimeField(null=True, blank=True)
    readme = models.TextField(blank=True)
    first_seen_at = models.DateTimeField(auto_now_add=True)
    last_scanned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-stars"]
        indexes = [
            models.Index(fields=["-stars"]),
            models.Index(fields=["language"]),
            models.Index(fields=["last_scanned_at"]),
        ]

    def __str__(self):
        return self.full_name


class RepositorySnapshot(models.Model):
    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="snapshots"
    )
    stars = models.PositiveIntegerField(default=0)
    forks = models.PositiveIntegerField(default=0)
    open_issues = models.PositiveIntegerField(default=0)
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-captured_at"]
        indexes = [
            models.Index(fields=["repository", "-captured_at"]),
        ]

    def __str__(self):
        return f"{self.repository.full_name} @ {self.captured_at:%Y-%m-%d}"
