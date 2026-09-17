from django.test import TestCase
from django.utils import timezone

from repositories.models import Repository

from .engine import (
    calculate_license_score,
    evaluate_repository,
)


class OpportunityEngineTests(TestCase):

    def test_permissive_license(self):
        self.assertEqual(
            calculate_license_score("MIT"),
            5,
        )

    def test_agro_repository_detection(self):
        repo = Repository.objects.create(
            github_id=999001,
            owner="teste",
            name="farm-manager",
            full_name="teste/farm-manager",
            url="https://github.com/teste/farm-manager",
            description=(
                "Farm agriculture livestock "
                "management SaaS platform"
            ),
            language="Python",
            topics=[
                "agriculture",
                "farm",
                "livestock",
            ],
            stars=1500,
            forks=150,
            open_issues=20,
            license_spdx="MIT",
            pushed_at_github=timezone.now(),
        )

        result = evaluate_repository(repo)

        self.assertEqual(
            result["rule"]["name"],
            "Agronegócio",
        )

        self.assertLessEqual(
            result["final_score"],
            100,
        )

        self.assertGreaterEqual(
            result["final_score"],
            60,
        )
