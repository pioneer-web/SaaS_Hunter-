from django.db import models
from repositories.models import Repository

class Opportunity(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Nova"
        WATCH = "watch", "Acompanhar"
        INVESTIGATE = "investigate", "Investigar"
        BUILD = "build", "Desenvolver"
        DISCARDED = "discarded", "Descartada"

    repository = models.OneToOneField(
        Repository, on_delete=models.CASCADE, related_name="opportunity"
    )
    problem = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    target_customer = models.TextField(blank=True)
    market_segment = models.CharField(max_length=255, blank=True)
    business_model = models.CharField(max_length=255, blank=True)
    suggested_pricing = models.CharField(max_length=255, blank=True)
    commercial_summary = models.TextField(blank=True)
    saas_possible = models.BooleanField(default=False)
    white_label_possible = models.BooleanField(default=False)
    api_possible = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.repository.full_name


class OpportunityScore(models.Model):
    opportunity = models.OneToOneField(
        Opportunity, on_delete=models.CASCADE, related_name="score"
    )
    market_problem = models.PositiveSmallIntegerField(default=0)
    monetization = models.PositiveSmallIntegerField(default=0)
    recurrence = models.PositiveSmallIntegerField(default=0)
    growth = models.PositiveSmallIntegerField(default=0)
    technical_maturity = models.PositiveSmallIntegerField(default=0)
    competition = models.PositiveSmallIntegerField(default=0)
    commercial_ease = models.PositiveSmallIntegerField(default=0)
    license = models.PositiveSmallIntegerField(default=0)
    differentiation = models.PositiveSmallIntegerField(default=0)
    final_score = models.PositiveSmallIntegerField(default=0)
    rationale = models.TextField(blank=True)
    calculated_at = models.DateTimeField(auto_now=True)

    def recalculate(self):
        self.final_score = min(
            100,
            self.market_problem
            + self.monetization
            + self.recurrence
            + self.growth
            + self.technical_maturity
            + self.competition
            + self.commercial_ease
            + self.license
            + self.differentiation,
        )
        return self.final_score

    def save(self, *args, **kwargs):
        self.recalculate()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.opportunity} - {self.final_score}/100"
