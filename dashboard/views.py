from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from opportunities.models import Opportunity
from repositories.models import Repository

@login_required
def home(request):
    context = {
        "repositories_count": Repository.objects.count(),
        "opportunities_count": Opportunity.objects.count(),
        "strong_opportunities_count": Opportunity.objects.filter(score__final_score__gte=80).count(),
        "recent_opportunities": Opportunity.objects.select_related("repository").order_by("-created_at")[:10],
    }
    return render(request, "dashboard/home.html", context)
