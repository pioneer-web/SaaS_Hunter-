from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.decorators.http import require_POST

from opportunities.engine import score_dimensions
from opportunities.models import (
    MarketAnalysis,
    Opportunity,
    OpportunityScore,
)
from opportunities.tasks import (
    research_opportunity_market_task,
)
from repositories.models import Repository
from scanner.tasks import discover_repositories


def attach_dimensions(item):
    try:
        score = item.score

    except OpportunityScore.DoesNotExist:
        item.commercial_score = None
        item.technical_score = None
        return item

    dimensions = score_dimensions(score)

    item.commercial_score = dimensions[
        "commercial_score"
    ]

    item.technical_score = dimensions[
        "technical_score"
    ]

    return item


@login_required
def home(request):
    repositories = Repository.objects.all()

    opportunities = (
        Opportunity.objects
        .select_related(
            "repository",
            "score",
        )
    )

    recent_opportunities = list(
        opportunities.order_by(
            "-score__final_score",
            "-created_at",
        )[:8]
    )

    for item in recent_opportunities:
        attach_dimensions(item)

    context = {
        "repositories_count": repositories.count(),

        "opportunities_count": opportunities.count(),

        "strong_opportunities_count": (
            opportunities
            .filter(
                score__final_score__gte=80
            )
            .count()
        ),

        "top_repositories": (
            repositories
            .order_by("-stars")[:8]
        ),

        "recent_opportunities": recent_opportunities,
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )


@login_required
def repositories_page(request):
    queryset = Repository.objects.all()

    q = request.GET.get(
        "q",
        "",
    ).strip()

    language = request.GET.get(
        "language",
        "",
    ).strip()

    if q:
        queryset = queryset.filter(
            Q(full_name__icontains=q)
            | Q(description__icontains=q)
            | Q(language__icontains=q)
        )

    if language:
        queryset = queryset.filter(
            language__iexact=language
        )

    languages = (
        Repository.objects
        .exclude(language="")
        .values_list(
            "language",
            flat=True,
        )
        .distinct()
        .order_by("language")
    )

    paginator = Paginator(
        queryset.order_by("-stars"),
        25,
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "dashboard/repositories.html",
        {
            "page_obj": page_obj,
            "q": q,
            "language": language,
            "languages": languages,
        },
    )


@login_required
def opportunities_page(request):
    queryset = (
        Opportunity.objects
        .select_related(
            "repository",
            "score",
        )
    )

    q = request.GET.get(
        "q",
        "",
    ).strip()

    status = request.GET.get(
        "status",
        "",
    ).strip()

    if q:
        queryset = queryset.filter(
            Q(repository__full_name__icontains=q)
            | Q(market_segment__icontains=q)
            | Q(target_customer__icontains=q)
            | Q(commercial_summary__icontains=q)
        )

    if status:
        queryset = queryset.filter(
            status=status
        )

    queryset = queryset.order_by(
        "-score__final_score",
        "-created_at",
    )

    paginator = Paginator(
        queryset,
        25,
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    for item in page_obj.object_list:
        attach_dimensions(item)

    return render(
        request,
        "dashboard/opportunities.html",
        {
            "page_obj": page_obj,
            "q": q,
            "status": status,
            "statuses": Opportunity.Status.choices,
        },
    )


@login_required
def opportunity_detail(request, pk):
    opportunity = get_object_or_404(
        Opportunity.objects.select_related(
            "repository",
            "score",
        ),
        pk=pk,
    )

    attach_dimensions(opportunity)

    try:
        market_analysis = (
            opportunity.market_analysis
        )

    except MarketAnalysis.DoesNotExist:
        market_analysis = None

    competitors = (
        opportunity.competitors
        .all()[:15]
    )

    return render(
        request,
        "dashboard/opportunity_detail.html",
        {
            "item": opportunity,
            "market_analysis": market_analysis,
            "competitors": competitors,
        },
    )


@login_required
@require_POST
def run_market_research(
    request,
    pk,
):
    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
    )

    task = (
        research_opportunity_market_task
        .delay(opportunity.pk)
    )

    messages.success(
        request,
        (
            "Pesquisa de concorrentes iniciada. "
            f"Tarefa: {task.id[:8]}…"
        ),
    )

    return redirect(
        "dashboard:opportunity_detail",
        pk=opportunity.pk,
    )


@login_required
@require_POST
def run_scan(request):
    task = discover_repositories.delay()

    messages.success(
        request,
        (
            "Caça iniciada. "
            f"Tarefa: {task.id[:8]}… "
            "O motor de oportunidades será "
            "executado automaticamente."
        ),
    )

    return redirect(
        "dashboard:home"
    )
