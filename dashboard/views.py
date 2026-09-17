from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from opportunities.models import Opportunity
from repositories.models import Repository
from scanner.tasks import discover_repositories


@login_required
def home(request):
    repositories = Repository.objects.all()
    opportunities = Opportunity.objects.all()

    context = {
        "repositories_count": repositories.count(),
        "opportunities_count": opportunities.count(),
        "strong_opportunities_count": opportunities.filter(
            score__final_score__gte=80
        ).count(),

        "top_repositories": repositories.order_by("-stars")[:8],

        "recent_opportunities": opportunities.select_related(
            "repository"
        ).order_by("-created_at")[:8],
    }

    return render(request, "dashboard/home.html", context)


@login_required
def repositories_page(request):
    queryset = Repository.objects.all()

    q = request.GET.get("q", "").strip()
    language = request.GET.get("language", "").strip()

    if q:
        queryset = queryset.filter(
            Q(full_name__icontains=q)
            | Q(description__icontains=q)
            | Q(language__icontains=q)
        )

    if language:
        queryset = queryset.filter(language__iexact=language)

    languages = (
        Repository.objects.exclude(language="")
        .values_list("language", flat=True)
        .distinct()
        .order_by("language")
    )

    paginator = Paginator(queryset.order_by("-stars"), 25)
    page_obj = paginator.get_page(request.GET.get("page"))

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
    queryset = Opportunity.objects.select_related("repository")

    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    if q:
        queryset = queryset.filter(
            Q(repository__full_name__icontains=q)
            | Q(market_segment__icontains=q)
            | Q(target_customer__icontains=q)
            | Q(commercial_summary__icontains=q)
        )

    if status:
        queryset = queryset.filter(status=status)

    paginator = Paginator(queryset.order_by("-created_at"), 25)
    page_obj = paginator.get_page(request.GET.get("page"))

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
@require_POST
def run_scan(request):
    task = discover_repositories.delay()

    messages.success(
        request,
        f"Caça iniciada. Tarefa: {task.id[:8]}…"
    )

    return redirect("dashboard:home")
