import logging

from celery import shared_task
from django.db import transaction

from repositories.models import Repository

from .engine import save_repository_analysis


logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def analyze_repositories(self, limit=1000):
    queryset = (
        Repository.objects
        .filter(
            archived=False,
            is_fork=False,
        )
        .order_by("-stars")[:limit]
    )

    analyzed = 0
    created = 0
    updated = 0
    skipped = 0
    failed = 0

    for repository in queryset:
        try:
            with transaction.atomic():
                opportunity, was_created, result = (
                    save_repository_analysis(repository)
                )

            analyzed += 1

            if opportunity is None:
                skipped += 1

            elif was_created:
                created += 1

            else:
                updated += 1

        except Exception:
            failed += 1

            logger.exception(
                "Falha analisando %s",
                repository.full_name,
            )

    return {
        "analyzed": analyzed,
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
    }
