import os
from datetime import datetime

import requests
from django.utils import timezone

from repositories.models import Repository, RepositorySnapshot

API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
TOKEN = os.getenv("GITHUB_TOKEN", "")


def headers():
    data = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "SaaS-Hunter/0.1",
    }
    if TOKEN:
        data["Authorization"] = f"Bearer {TOKEN}"
    return data


def parse_dt(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def github_get(path, params=None):
    response = requests.get(
        f"{API_URL}{path}",
        params=params or {},
        headers=headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def search_repositories(
    query,
    per_page=30,
    sort="updated",
    order="desc",
):
    data = github_get(
        "/search/repositories",
        params={
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
        },
    )
    return data.get("items", [])


def fetch_repository(full_name):
    return github_get(f"/repos/{full_name}")


def upsert_repository(item):
    license_data = item.get("license") or {}
    defaults = {
        "owner": (item.get("owner") or {}).get("login", ""),
        "name": item.get("name", ""),
        "full_name": item.get("full_name", ""),
        "url": item.get("html_url", ""),
        "description": item.get("description") or "",
        "language": item.get("language") or "",
        "topics": item.get("topics") or [],
        "stars": item.get("stargazers_count") or 0,
        "forks": item.get("forks_count") or 0,
        "watchers": item.get("watchers_count") or 0,
        "open_issues": item.get("open_issues_count") or 0,
        "license_spdx": license_data.get("spdx_id") or "",
        "is_fork": bool(item.get("fork")),
        "archived": bool(item.get("archived")),
        "created_at_github": parse_dt(item.get("created_at")),
        "updated_at_github": parse_dt(item.get("updated_at")),
        "pushed_at_github": parse_dt(item.get("pushed_at")),
        "last_scanned_at": timezone.now(),
    }
    repository, _ = Repository.objects.update_or_create(
        github_id=item["id"], defaults=defaults
    )
    RepositorySnapshot.objects.create(
        repository=repository,
        stars=repository.stars,
        forks=repository.forks,
        open_issues=repository.open_issues,
    )
    return repository
