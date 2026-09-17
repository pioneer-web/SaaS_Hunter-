from django.contrib import admin
from .models import Repository, RepositorySnapshot

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "language", "stars", "forks", "license_spdx", "archived")
    search_fields = ("full_name", "description")
    list_filter = ("language", "archived", "is_fork", "license_spdx")

@admin.register(RepositorySnapshot)
class RepositorySnapshotAdmin(admin.ModelAdmin):
    list_display = ("repository", "stars", "forks", "open_issues", "captured_at")
    search_fields = ("repository__full_name",)
