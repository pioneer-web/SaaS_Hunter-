import uuid
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Repository",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("github_id", models.BigIntegerField(unique=True)),
                ("owner", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("full_name", models.CharField(max_length=520, unique=True)),
                ("url", models.URLField(max_length=1000)),
                ("description", models.TextField(blank=True)),
                ("language", models.CharField(blank=True, max_length=120)),
                ("topics", models.JSONField(blank=True, default=list)),
                ("stars", models.PositiveIntegerField(default=0)),
                ("forks", models.PositiveIntegerField(default=0)),
                ("watchers", models.PositiveIntegerField(default=0)),
                ("open_issues", models.PositiveIntegerField(default=0)),
                ("license_spdx", models.CharField(blank=True, max_length=80)),
                ("is_fork", models.BooleanField(default=False)),
                ("archived", models.BooleanField(default=False)),
                ("created_at_github", models.DateTimeField(blank=True, null=True)),
                ("updated_at_github", models.DateTimeField(blank=True, null=True)),
                ("pushed_at_github", models.DateTimeField(blank=True, null=True)),
                ("readme", models.TextField(blank=True)),
                ("first_seen_at", models.DateTimeField(auto_now_add=True)),
                ("last_scanned_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={"ordering": ["-stars"]},
        ),
        migrations.CreateModel(
            name="RepositorySnapshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("stars", models.PositiveIntegerField(default=0)),
                ("forks", models.PositiveIntegerField(default=0)),
                ("open_issues", models.PositiveIntegerField(default=0)),
                ("captured_at", models.DateTimeField(auto_now_add=True)),
                ("repository", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="snapshots", to="repositories.repository")),
            ],
            options={"ordering": ["-captured_at"]},
        ),
        migrations.AddIndex(
            model_name="repository",
            index=models.Index(fields=["-stars"], name="repositori_stars_idx"),
        ),
        migrations.AddIndex(
            model_name="repository",
            index=models.Index(fields=["language"], name="repositori_lang_idx"),
        ),
        migrations.AddIndex(
            model_name="repository",
            index=models.Index(fields=["last_scanned_at"], name="repositori_scan_idx"),
        ),
        migrations.AddIndex(
            model_name="repositorysnapshot",
            index=models.Index(fields=["repository", "-captured_at"], name="repo_snap_repo_time_idx"),
        ),
    ]
