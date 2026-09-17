from django.test import TestCase
from django.utils import timezone

from repositories.models import Repository

from .engine import (
    calculate_license_score,
    evaluate_repository,
)


class OpportunityEngineTests(TestCase):

    def make_repo(
        self,
        github_id,
        name,
        description,
        topics,
        stars=1000,
        forks=100,
        license_spdx="MIT",
    ):
        return Repository.objects.create(
            github_id=github_id,
            owner="teste",
            name=name,
            full_name=f"teste/{name}",
            url=f"https://github.com/teste/{name}",
            description=description,
            language="Python",
            topics=topics,
            stars=stars,
            forks=forks,
            open_issues=20,
            license_spdx=license_spdx,
            pushed_at_github=timezone.now(),
        )

    def test_permissive_license(self):
        self.assertEqual(
            calculate_license_score("MIT"),
            5,
        )

    def test_unknown_license(self):
        self.assertEqual(
            calculate_license_score(""),
            0,
        )

    def test_agro_repository_detection(self):
        repo = self.make_repo(
            9001,
            "tania-core",
            (
                "Farm management software "
                "for smallholder farmers"
            ),
            [
                "farm",
                "farm-management",
                "farming",
            ],
        )

        result = evaluate_repository(repo)

        self.assertEqual(
            result["rule"]["name"],
            "Agronegócio",
        )

    def test_crm_beats_ai_feature(self):
        repo = self.make_repo(
            9002,
            "DeskcommCRM",
            (
                "Open-source AI sales OS. "
                "Self-hosted CRM with native AI agents "
                "and WhatsApp."
            ),
            [
                "ai",
                "ai-agents",
                "crm",
                "sales-automation",
                "whatsapp",
                "rag",
            ],
        )

        result = evaluate_repository(repo)

        self.assertEqual(
            result["rule"]["name"],
            "CRM e Vendas",
        )

    def test_erp_beats_finance_topics(self):
        repo = self.make_repo(
            9003,
            "ever-gauzy",
            (
                "Open Business Management Platform "
                "ERP CRM HRM ATS PM"
            ),
            [
                "accounting",
                "billing",
                "bookkeeping",
                "expenses",
                "invoices",
                "erp",
                "crm",
            ],
            license_spdx="AGPL-3.0",
        )

        result = evaluate_repository(repo)

        self.assertEqual(
            result["rule"]["name"],
            "Gestão Empresarial / ERP",
        )

    def test_ai_can_be_primary_when_no_vertical_exists(self):
        repo = self.make_repo(
            9004,
            "agent-platform",
            (
                "AI agent platform for building "
                "LLM automation and RAG assistants"
            ),
            [
                "ai-agent",
                "llm",
                "rag",
            ],
        )

        result = evaluate_repository(repo)

        self.assertEqual(
            result["rule"]["name"],
            "IA e Automação",
        )

    def test_scores_never_exceed_100(self):
        repo = self.make_repo(
            9005,
            "farm-saas",
            (
                "Farm management SaaS platform "
                "with billing and subscription"
            ),
            [
                "farm",
                "farming",
                "agriculture",
                "saas",
            ],
            stars=20000,
            forks=3000,
        )

        result = evaluate_repository(repo)

        self.assertLessEqual(
            result["final_score"],
            100,
        )

        self.assertLessEqual(
            result["commercial_score"],
            100,
        )

        self.assertLessEqual(
            result["technical_score"],
            100,
        )
