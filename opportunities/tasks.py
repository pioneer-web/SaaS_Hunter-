import logging
import time

from celery import shared_task
from django.db import transaction

from repositories.models import Repository
from scanner.github import TOKEN

from .engine import (
    save_repository_analysis,
)
from .market import (
    research_opportunity_market,
)
from .models import Opportunity


logger = logging.getLogger(
    __name__
)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def analyze_repositories(
    self,
    limit=1000,
):
    queryset = (
        Repository.objects
        .filter(
            archived=False,
            is_fork=False,
        )
        .order_by(
            "-stars"
        )[:limit]
    )

    analyzed = 0
    created = 0
    updated = 0
    skipped = 0
    failed = 0

    for repository in queryset:
        try:

            with transaction.atomic():
                (
                    opportunity,
                    was_created,
                    result,
                ) = save_repository_analysis(
                    repository
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


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def research_opportunity_market_task(
    self,
    opportunity_id,
):
    opportunity = (
        Opportunity.objects
        .select_related(
            "repository",
            "score",
        )
        .get(
            pk=opportunity_id
        )
    )

    analysis = (
        research_opportunity_market(
            opportunity
        )
    )

    return {
        "opportunity": (
            opportunity
            .repository
            .full_name
        ),
        "competitors": (
            analysis
            .open_source_competitors
        ),
        "strong": (
            analysis
            .strong_open_source_competitors
        ),
        "saturation": (
            analysis
            .saturation_score
        ),
    }


@shared_task(
    bind=True,
)
def research_top_opportunities(
    self,
    limit=8,
):
    queryset = (
        Opportunity.objects
        .select_related(
            "repository",
            "score",
        )
        .filter(
            score__final_score__gte=75
        )
        .order_by(
            "-score__final_score"
        )[:limit]
    )

    researched = 0
    failed = 0
    results = []

    opportunities = list(
        queryset
    )

    for index, opportunity in enumerate(
        opportunities
    ):

        try:
            analysis = (
                research_opportunity_market(
                    opportunity
                )
            )

            researched += 1

            results.append(
                {
                    "name": (
                        opportunity
                        .repository
                        .full_name
                    ),
                    "competitors": (
                        analysis
                        .open_source_competitors
                    ),
                    "strong": (
                        analysis
                        .strong_open_source_competitors
                    ),
                    "saturation": (
                        analysis
                        .saturation_score
                    ),
                    "level": (
                        analysis
                        .get_saturation_level_display()
                    ),
                }
            )

        except Exception:
            failed += 1

            logger.exception(
                "Falha na pesquisa de mercado de %s",
                opportunity.repository.full_name,
            )

        # GitHub Search possui limite próprio.
        # Sem token, espaçamos as consultas.
        if (
            not TOKEN
            and index
            < len(opportunities) - 1
        ):
            time.sleep(7)

    return {
        "researched": researched,
        "failed": failed,
        "results": results,
    }
