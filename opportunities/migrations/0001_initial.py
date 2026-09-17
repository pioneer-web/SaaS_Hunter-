from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("repositories", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Opportunity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("problem", models.TextField(blank=True)),
                ("solution", models.TextField(blank=True)),
                ("target_customer", models.TextField(blank=True)),
                ("market_segment", models.CharField(blank=True, max_length=255)),
                ("business_model", models.CharField(blank=True, max_length=255)),
                ("suggested_pricing", models.CharField(blank=True, max_length=255)),
                ("commercial_summary", models.TextField(blank=True)),
                ("saas_possible", models.BooleanField(default=False)),
                ("white_label_possible", models.BooleanField(default=False)),
                ("api_possible", models.BooleanField(default=False)),
                ("status", models.CharField(choices=[("new","Nova"),("watch","Acompanhar"),("investigate","Investigar"),("build","Desenvolver"),("discarded","Descartada")], default="new", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("repository", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="opportunity", to="repositories.repository")),
            ],
        ),
        migrations.CreateModel(
            name="OpportunityScore",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("market_problem", models.PositiveSmallIntegerField(default=0)),
                ("monetization", models.PositiveSmallIntegerField(default=0)),
                ("recurrence", models.PositiveSmallIntegerField(default=0)),
                ("growth", models.PositiveSmallIntegerField(default=0)),
                ("technical_maturity", models.PositiveSmallIntegerField(default=0)),
                ("competition", models.PositiveSmallIntegerField(default=0)),
                ("commercial_ease", models.PositiveSmallIntegerField(default=0)),
                ("license", models.PositiveSmallIntegerField(default=0)),
                ("differentiation", models.PositiveSmallIntegerField(default=0)),
                ("final_score", models.PositiveSmallIntegerField(default=0)),
                ("rationale", models.TextField(blank=True)),
                ("calculated_at", models.DateTimeField(auto_now=True)),
                ("opportunity", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="score", to="opportunities.opportunity")),
            ],
        ),
    ]
