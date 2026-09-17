from celery import shared_task
from django.db import transaction

from repositories.models import Repository
from .github import fetch_repository, search_repositories, upsert_repository

DEFAULT_QUERIES = [
    "topic:saas stars:>20 archived:false",
    "crm stars:>30 archived:false",
    "erp stars:>30 archived:false",
    "\"booking system\" stars:>30 archived:false",
    "\"clinic management\" stars:>20 archived:false",
    "\"farm management\" stars:>10 archived:false",
    "\"property management\" stars:>20 archived:false",
    "\"gym management\" stars:>10 archived:false",
    "\"ai agent\" stars:>100 archived:false",
]


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def discover_repositories(self):
    processed = 0
    for query in DEFAULT_QUERIES:
        for item in search_repositories(query, per_page=30):
            with transaction.atomic():
                upsert_repository(item)
            processed += 1
    return {"processed": processed}


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def refresh_repository_snapshots(self):
    refreshed = 0
    failed = 0

    for repo in Repository.objects.filter(archived=False).iterator():
        try:
            item = fetch_repository(repo.full_name)
            with transaction.atomic():
                upsert_repository(item)
            refreshed += 1
        except Exception:
            failed += 1

    return {"refreshed": refreshed, "failed": failed}
