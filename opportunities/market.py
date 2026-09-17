from datetime import timedelta

from django.utils import timezone

from scanner.github import (
    parse_dt,
    search_repositories,
)

from .models import (
    Competitor,
    MarketAnalysis,
)


MARKET_CONFIG = {

    "Agronegócio": {
        "query": (
            '"farm management" '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "farm management",
            "farming",
            "agriculture",
            "livestock",
            "farm",
        ),
    },

    "Saúde e Clínicas": {
        "query": (
            '"clinic management" '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "clinic",
            "clinical",
            "patient",
            "healthcare",
            "medical",
        ),
    },

    "Academias e Fitness": {
        "query": (
            '"gym management" '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "gym",
            "fitness",
            "workout",
            "trainer",
        ),
    },

    "Imobiliário": {
        "query": (
            '"property management" '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "property management",
            "real estate",
            "rental",
            "tenant",
            "property",
        ),
    },

    "Agendamento e Reservas": {
        "query": (
            '"booking system" '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "booking",
            "appointment",
            "reservation",
            "scheduling",
        ),
    },

    "CRM e Vendas": {
        "query": (
            'crm sales '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "crm",
            "sales",
            "lead",
            "pipeline",
            "customer",
        ),
    },

    "Gestão Empresarial / ERP": {
        "query": (
            'erp '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "erp",
            "business management",
            "enterprise resource",
            "inventory",
        ),
    },

    "Comércio e E-commerce": {
        "query": (
            'ecommerce '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "ecommerce",
            "e-commerce",
            "store",
            "commerce",
            "retail",
        ),
    },

    "Finanças e Gestão Financeira": {
        "query": (
            'finance saas '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "finance",
            "financial",
            "fintech",
            "billing",
            "accounting",
            "invoice",
        ),
    },

    "Educação": {
        "query": (
            '"learning management" '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "learning management",
            "education",
            "school",
            "student",
            "lms",
        ),
    },

    "Documentos e Workflows": {
        "query": (
            '"document management" '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "document",
            "workflow",
            "approval",
            "forms",
        ),
    },

    "IA e Automação": {
        "query": (
            '"ai agent" '
            'in:name,description '
            'archived:false fork:false'
        ),
        "keywords": (
            "ai agent",
            "llm",
            "rag",
            "automation",
            "assistant",
        ),
    },
}


def normalize(value):
    value = (value or "").lower()

    for char in (
        "-",
        "_",
        "/",
        ".",
        ",",
        "(",
        ")",
        "[",
        "]",
        ":",
    ):
        value = value.replace(
            char,
            " ",
        )

    return " ".join(
        value.split()
    )


def item_text(item):
    topics = item.get(
        "topics"
    ) or []

    return normalize(
        " ".join(
            [
                item.get(
                    "name",
                    "",
                ),
                item.get(
                    "full_name",
                    "",
                ),
                item.get(
                    "description",
                    "",
                ) or "",
                " ".join(
                    str(topic)
                    for topic in topics
                ),
            ]
        )
    )


def relevance_score(
    opportunity,
    item,
    keywords,
):
    text = item_text(item)

    hits = 0

    for keyword in keywords:
        if normalize(keyword) in text:
            hits += 1

    score = 20

    score += min(
        50,
        hits * 10,
    )

    stars = (
        item.get(
            "stargazers_count"
        )
        or 0
    )

    if stars >= 10000:
        score += 15

    elif stars >= 3000:
        score += 12

    elif stars >= 1000:
        score += 10

    elif stars >= 300:
        score += 7

    elif stars >= 50:
        score += 4

    language = (
        item.get("language")
        or ""
    )

    if (
        language
        and opportunity.repository.language
        and language.lower()
        == opportunity.repository.language.lower()
    ):
        score += 5

    return min(
        100,
        score,
    )


def is_strong_competitor(
    item,
    relevance,
):
    stars = (
        item.get(
            "stargazers_count"
        )
        or 0
    )

    pushed_at = parse_dt(
        item.get(
            "pushed_at"
        )
    )

    if not pushed_at:
        return False

    active = (
        timezone.now()
        - pushed_at
    ) <= timedelta(
        days=365
    )

    return (
        relevance >= 45
        and stars >= 500
        and active
    )


def calculate_saturation(
    competitor_count,
    strong_count,
    top_stars,
):
    star_component = 0

    if top_stars >= 20000:
        star_component = 20

    elif top_stars >= 10000:
        star_component = 16

    elif top_stars >= 5000:
        star_component = 12

    elif top_stars >= 1000:
        star_component = 8

    elif top_stars >= 250:
        star_component = 4

    score = min(
        100,
        (
            competitor_count * 2
            + strong_count * 8
            + star_component
        ),
    )

    if score < 30:
        level = (
            MarketAnalysis
            .Saturation
            .LOW
        )

    elif score < 55:
        level = (
            MarketAnalysis
            .Saturation
            .MEDIUM
        )

    elif score < 80:
        level = (
            MarketAnalysis
            .Saturation
            .HIGH
        )

    else:
        level = (
            MarketAnalysis
            .Saturation
            .VERY_HIGH
        )

    return score, level


def research_opportunity_market(
    opportunity,
):
    config = MARKET_CONFIG.get(
        opportunity.market_segment
    )

    if not config:
        analysis, _ = (
            MarketAnalysis.objects
            .update_or_create(
                opportunity=opportunity,
                defaults={
                    "query_used": "",
                    "open_source_competitors": 0,
                    "strong_open_source_competitors": 0,
                    "saturation_score": 0,
                    "saturation_level": (
                        MarketAnalysis
                        .Saturation
                        .LOW
                    ),
                    "top_competitor_name": "",
                    "top_competitor_url": "",
                    "top_competitor_stars": 0,
                    "summary": (
                        "Este nicho ainda não possui "
                        "uma consulta especializada "
                        "na versão 0.4."
                    ),
                },
            )
        )

        return analysis

    query = config["query"]

    items = search_repositories(
        query,
        per_page=30,
        sort="stars",
        order="desc",
    )

    candidates = []

    for item in items:

        if (
            item.get("full_name")
            == opportunity.repository.full_name
        ):
            continue

        relevance = relevance_score(
            opportunity,
            item,
            config["keywords"],
        )

        # Evita armazenar resultado muito fraco.
        if relevance < 30:
            continue

        strong = is_strong_competitor(
            item,
            relevance,
        )

        candidates.append(
            {
                "item": item,
                "relevance": relevance,
                "strong": strong,
            }
        )

    candidates.sort(
        key=lambda value: (
            value["relevance"],
            value["item"].get(
                "stargazers_count"
            )
            or 0,
        ),
        reverse=True,
    )

    Competitor.objects.filter(
        opportunity=opportunity
    ).delete()

    for candidate in candidates:

        item = candidate["item"]

        license_data = (
            item.get("license")
            or {}
        )

        Competitor.objects.create(
            opportunity=opportunity,
            github_id=item["id"],
            full_name=item.get(
                "full_name",
                "",
            ),
            url=item.get(
                "html_url",
                "",
            ),
            description=(
                item.get(
                    "description"
                )
                or ""
            ),
            language=(
                item.get(
                    "language"
                )
                or ""
            ),
            stars=(
                item.get(
                    "stargazers_count"
                )
                or 0
            ),
            forks=(
                item.get(
                    "forks_count"
                )
                or 0
            ),
            open_issues=(
                item.get(
                    "open_issues_count"
                )
                or 0
            ),
            license_spdx=(
                license_data.get(
                    "spdx_id"
                )
                or ""
            ),
            relevance_score=(
                candidate[
                    "relevance"
                ]
            ),
            is_strong=(
                candidate[
                    "strong"
                ]
            ),
            pushed_at_github=parse_dt(
                item.get(
                    "pushed_at"
                )
            ),
        )

    competitor_count = len(
        candidates
    )

    strong_count = sum(
        1
        for candidate
        in candidates
        if candidate["strong"]
    )

    top = (
        candidates[0]
        if candidates
        else None
    )

    top_stars = (
        top["item"].get(
            "stargazers_count"
        )
        or 0
        if top
        else 0
    )

    saturation_score, saturation_level = (
        calculate_saturation(
            competitor_count,
            strong_count,
            top_stars,
        )
    )

    if competitor_count == 0:
        summary = (
            "Nenhuma alternativa open-source "
            "relevante foi encontrada nesta consulta. "
            "Isso não significa ausência de concorrência comercial."
        )

    else:
        summary = (
            f"Foram encontradas "
            f"{competitor_count} alternativas open-source "
            f"relevantes no GitHub, sendo "
            f"{strong_count} classificadas como fortes. "
            f"O índice de saturação open-source é "
            f"{saturation_score}/100. "
            "Este indicador mede apenas o ecossistema "
            "open-source pesquisado e não representa, sozinho, "
            "o tamanho ou a saturação do mercado comercial."
        )

    analysis, _ = (
        MarketAnalysis.objects
        .update_or_create(
            opportunity=opportunity,
            defaults={
                "query_used": query,
                "open_source_competitors": (
                    competitor_count
                ),
                "strong_open_source_competitors": (
                    strong_count
                ),
                "saturation_score": (
                    saturation_score
                ),
                "saturation_level": (
                    saturation_level
                ),
                "top_competitor_name": (
                    top["item"].get(
                        "full_name",
                        "",
                    )
                    if top
                    else ""
                ),
                "top_competitor_url": (
                    top["item"].get(
                        "html_url",
                        "",
                    )
                    if top
                    else ""
                ),
                "top_competitor_stars": (
                    top_stars
                ),
                "summary": summary,
            },
        )
    )

    return analysis
