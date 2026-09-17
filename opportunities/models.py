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

# =========================================================
# SaaS Hunter 0.4 - Market Intelligence
# =========================================================

class MarketAnalysis(models.Model):
    class Saturation(models.TextChoices):
        LOW = "low", "Baixa"
        MEDIUM = "medium", "Média"
        HIGH = "high", "Alta"
        VERY_HIGH = "very_high", "Muito alta"

    opportunity = models.OneToOneField(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="market_analysis",
    )

    query_used = models.CharField(
        max_length=500,
        blank=True,
    )

    open_source_competitors = models.PositiveIntegerField(
        default=0
    )

    strong_open_source_competitors = models.PositiveIntegerField(
        default=0
    )

    saturation_score = models.PositiveSmallIntegerField(
        default=0
    )

    saturation_level = models.CharField(
        max_length=20,
        choices=Saturation.choices,
        default=Saturation.LOW,
    )

    top_competitor_name = models.CharField(
        max_length=520,
        blank=True,
    )

    top_competitor_url = models.URLField(
        max_length=1000,
        blank=True,
    )

    top_competitor_stars = models.PositiveIntegerField(
        default=0
    )

    summary = models.TextField(
        blank=True
    )

    researched_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.opportunity.repository.full_name} - "
            f"{self.get_saturation_level_display()}"
        )


class Competitor(models.Model):
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="competitors",
    )

    github_id = models.BigIntegerField()

    full_name = models.CharField(
        max_length=520
    )

    url = models.URLField(
        max_length=1000
    )

    description = models.TextField(
        blank=True
    )

    language = models.CharField(
        max_length=120,
        blank=True,
    )

    stars = models.PositiveIntegerField(
        default=0
    )

    forks = models.PositiveIntegerField(
        default=0
    )

    open_issues = models.PositiveIntegerField(
        default=0
    )

    license_spdx = models.CharField(
        max_length=80,
        blank=True,
    )

    relevance_score = models.PositiveSmallIntegerField(
        default=0
    )

    is_strong = models.BooleanField(
        default=False
    )

    pushed_at_github = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-relevance_score",
            "-stars",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "opportunity",
                    "github_id",
                ],
                name="unique_opportunity_competitor",
            )
        ]

        indexes = [
            models.Index(
                fields=[
                    "opportunity",
                    "-relevance_score",
                ]
            ),
            models.Index(
                fields=["-stars"]
            ),
        ]

    def __str__(self):
        return self.full_name

# =========================================================
# SaaS Hunter 0.4 - Market Intelligence
# =========================================================

class MarketAnalysis(models.Model):
    class Saturation(models.TextChoices):
        LOW = "low", "Baixa"
        MEDIUM = "medium", "Média"
        HIGH = "high", "Alta"
        VERY_HIGH = "very_high", "Muito alta"

    opportunity = models.OneToOneField(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="market_analysis",
    )

    query_used = models.CharField(
        max_length=500,
        blank=True,
    )

    open_source_competitors = models.PositiveIntegerField(
        default=0
    )

    strong_open_source_competitors = models.PositiveIntegerField(
        default=0
    )

    saturation_score = models.PositiveSmallIntegerField(
        default=0
    )

    saturation_level = models.CharField(
        max_length=20,
        choices=Saturation.choices,
        default=Saturation.LOW,
    )

    top_competitor_name = models.CharField(
        max_length=520,
        blank=True,
    )

    top_competitor_url = models.URLField(
        max_length=1000,
        blank=True,
    )

    top_competitor_stars = models.PositiveIntegerField(
        default=0
    )

    summary = models.TextField(
        blank=True
    )

    researched_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.opportunity.repository.full_name} - "
            f"{self.get_saturation_level_display()}"
        )


class Competitor(models.Model):
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="competitors",
    )

    github_id = models.BigIntegerField()

    full_name = models.CharField(
        max_length=520
    )

    url = models.URLField(
        max_length=1000
    )

    description = models.TextField(
        blank=True
    )

    language = models.CharField(
        max_length=120,
        blank=True,
    )

    stars = models.PositiveIntegerField(
        default=0
    )

    forks = models.PositiveIntegerField(
        default=0
    )

    open_issues = models.PositiveIntegerField(
        default=0
    )

    license_spdx = models.CharField(
        max_length=80,
        blank=True,
    )

    relevance_score = models.PositiveSmallIntegerField(
        default=0
    )

    is_strong = models.BooleanField(
        default=False
    )

    pushed_at_github = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-relevance_score",
            "-stars",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "opportunity",
                    "github_id",
                ],
                name="unique_opportunity_competitor",
            )
        ]

        indexes = [
            models.Index(
                fields=[
                    "opportunity",
                    "-relevance_score",
                ]
            ),
            models.Index(
                fields=["-stars"]
            ),
        ]

    def __str__(self):
        return self.full_name
