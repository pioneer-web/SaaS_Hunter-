from django.contrib import admin
from .models import Opportunity, OpportunityScore

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("repository", "market_segment", "status", "created_at")
    list_filter = ("status", "saas_possible", "white_label_possible", "api_possible")
    search_fields = ("repository__full_name", "market_segment", "commercial_summary")

@admin.register(OpportunityScore)
class OpportunityScoreAdmin(admin.ModelAdmin):
    list_display = ("opportunity", "final_score", "calculated_at")
    search_fields = ("opportunity__repository__full_name",)
