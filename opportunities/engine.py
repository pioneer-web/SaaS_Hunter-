from datetime import timedelta

from django.utils import timezone

from opportunities.models import Opportunity, OpportunityScore


MIN_OPPORTUNITY_SCORE = 60


CATEGORY_RULES = [
    {
        "slug": "agro",
        "name": "Agronegócio",
        "keywords": (
            "agriculture", "agricultural", "farm", "farming",
            "livestock", "rural", "agro", "crop", "cattle",
            "irrigation", "farmer",
        ),
        "problem": (
            "Produtores e empresas rurais precisam organizar operações, "
            "dados, controles e processos que muitas vezes ainda são manuais."
        ),
        "solution": (
            "Transformar o projeto em uma plataforma SaaS especializada "
            "para gestão e automação de operações do agronegócio."
        ),
        "target": "Produtores rurais, consultores, cooperativas e empresas do agronegócio",
        "business_model": "SaaS B2B vertical por assinatura",
        "pricing": "R$ 79 a R$ 399/mês",
        "market_problem": 18,
        "monetization": 17,
        "recurrence": 14,
        "competition": 8,
        "commercial_ease": 4,
        "differentiation": 4,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "health",
        "name": "Saúde e Clínicas",
        "keywords": (
            "clinic", "clinical", "hospital", "medical",
            "healthcare", "health", "patient", "doctor",
            "dental", "dentist", "veterinary", "veterinarian",
        ),
        "problem": (
            "Clínicas e profissionais precisam centralizar agenda, "
            "cadastros, atendimento, histórico e processos administrativos."
        ),
        "solution": (
            "Oferecer uma versão hospedada e simplificada como SaaS "
            "vertical para clínicas e profissionais."
        ),
        "target": "Clínicas, consultórios e profissionais de saúde",
        "business_model": "SaaS B2B por unidade ou profissional",
        "pricing": "R$ 69 a R$ 349/mês",
        "market_problem": 18,
        "monetization": 18,
        "recurrence": 15,
        "competition": 6,
        "commercial_ease": 4,
        "differentiation": 4,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "fitness",
        "name": "Academias e Fitness",
        "keywords": (
            "gym", "fitness", "workout", "trainer",
            "training", "exercise", "crossfit", "wellness",
        ),
        "problem": (
            "Academias e profissionais precisam gerenciar alunos, "
            "treinos, cobranças, agenda e relacionamento."
        ),
        "solution": (
            "Transformar o projeto em SaaS para academias, studios "
            "ou personal trainers."
        ),
        "target": "Academias, studios, boxes e personal trainers",
        "business_model": "SaaS B2B vertical",
        "pricing": "R$ 49 a R$ 299/mês",
        "market_problem": 17,
        "monetization": 18,
        "recurrence": 15,
        "competition": 6,
        "commercial_ease": 5,
        "differentiation": 4,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "property",
        "name": "Imobiliário",
        "keywords": (
            "property", "properties", "real estate",
            "realestate", "rental", "tenant", "landlord",
            "condominium", "housing",
        ),
        "problem": (
            "Imobiliárias, administradores e proprietários precisam "
            "controlar imóveis, contratos, clientes e cobranças."
        ),
        "solution": (
            "Oferecer uma plataforma SaaS para gestão imobiliária "
            "e administração de propriedades."
        ),
        "target": "Imobiliárias, administradores de imóveis e proprietários",
        "business_model": "SaaS B2B por carteira de imóveis",
        "pricing": "R$ 79 a R$ 499/mês",
        "market_problem": 17,
        "monetization": 18,
        "recurrence": 15,
        "competition": 6,
        "commercial_ease": 4,
        "differentiation": 4,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "booking",
        "name": "Agendamento e Reservas",
        "keywords": (
            "booking", "appointment", "appointments",
            "reservation", "reservations", "scheduling",
            "scheduler", "calendar",
        ),
        "problem": (
            "Pequenos negócios precisam reduzir atendimento manual "
            "e organizar horários, reservas e confirmações."
        ),
        "solution": (
            "Transformar o projeto em plataforma de agendamento "
            "online por assinatura."
        ),
        "target": "Prestadores de serviço, salões, clínicas, studios e pequenos negócios",
        "business_model": "Micro-SaaS B2B por estabelecimento",
        "pricing": "R$ 29 a R$ 149/mês",
        "market_problem": 17,
        "monetization": 17,
        "recurrence": 15,
        "competition": 5,
        "commercial_ease": 5,
        "differentiation": 3,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "crm",
        "name": "CRM e Vendas",
        "keywords": (
            "crm", "customer relationship", "sales",
            "sales pipeline", "lead", "leads", "pipeline",
            "customer management",
        ),
        "problem": (
            "Empresas precisam organizar leads, negociações, "
            "clientes e atividades comerciais."
        ),
        "solution": (
            "Criar uma versão SaaS hospedada, simples e especializada "
            "para gestão comercial."
        ),
        "target": "Pequenas e médias empresas e equipes comerciais",
        "business_model": "SaaS B2B por usuário ou equipe",
        "pricing": "R$ 39 a R$ 249/mês",
        "market_problem": 16,
        "monetization": 18,
        "recurrence": 15,
        "competition": 4,
        "commercial_ease": 4,
        "differentiation": 3,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "erp",
        "name": "Gestão Empresarial / ERP",
        "keywords": (
            "erp", "enterprise resource", "business management",
            "inventory management", "business administration",
            "management system", "backoffice",
        ),
        "problem": (
            "Pequenas empresas precisam integrar processos administrativos, "
            "financeiros, estoque e operação."
        ),
        "solution": (
            "Transformar o projeto em ERP SaaS simplificado ou "
            "especializado em um nicho."
        ),
        "target": "Pequenas e médias empresas",
        "business_model": "SaaS B2B por empresa",
        "pricing": "R$ 79 a R$ 499/mês",
        "market_problem": 17,
        "monetization": 18,
        "recurrence": 15,
        "competition": 4,
        "commercial_ease": 4,
        "differentiation": 3,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "ecommerce",
        "name": "Comércio e E-commerce",
        "keywords": (
            "ecommerce", "e-commerce", "shopping cart",
            "store", "online store", "commerce",
            "marketplace", "retail", "pos",
        ),
        "problem": (
            "Lojistas precisam vender, gerenciar pedidos, produtos, "
            "clientes e operação digital."
        ),
        "solution": (
            "Criar serviço SaaS hospedado para comércio eletrônico "
            "ou gestão de vendas."
        ),
        "target": "Lojas, pequenos varejistas e vendedores online",
        "business_model": "SaaS + possíveis taxas por transação",
        "pricing": "R$ 49 a R$ 299/mês",
        "market_problem": 16,
        "monetization": 18,
        "recurrence": 14,
        "competition": 4,
        "commercial_ease": 4,
        "differentiation": 3,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "finance",
        "name": "Finanças e Gestão Financeira",
        "keywords": (
            "finance", "financial", "accounting",
            "invoice", "billing", "expense", "expenses",
            "cashflow", "cash flow", "bookkeeping",
        ),
        "problem": (
            "Empresas e profissionais precisam controlar receitas, "
            "despesas, cobranças e indicadores financeiros."
        ),
        "solution": (
            "Transformar o projeto em plataforma financeira SaaS "
            "com automações e relatórios."
        ),
        "target": "Pequenas empresas, escritórios e profissionais autônomos",
        "business_model": "SaaS B2B por empresa",
        "pricing": "R$ 39 a R$ 249/mês",
        "market_problem": 18,
        "monetization": 18,
        "recurrence": 15,
        "competition": 5,
        "commercial_ease": 4,
        "differentiation": 3,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "education",
        "name": "Educação",
        "keywords": (
            "education", "school", "student",
            "learning management", "lms", "course",
            "classroom", "teacher", "learning",
        ),
        "problem": (
            "Instituições e educadores precisam organizar alunos, "
            "conteúdo, acompanhamento e pagamentos."
        ),
        "solution": (
            "Criar plataforma SaaS para cursos, escolas "
            "ou treinamento corporativo."
        ),
        "target": "Escolas, cursos, professores e empresas de treinamento",
        "business_model": "SaaS por instituição ou número de alunos",
        "pricing": "R$ 49 a R$ 299/mês",
        "market_problem": 16,
        "monetization": 17,
        "recurrence": 14,
        "competition": 6,
        "commercial_ease": 4,
        "differentiation": 4,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "documents",
        "name": "Documentos e Workflows",
        "keywords": (
            "document management", "documents", "document",
            "workflow", "approval", "forms",
            "form builder", "pdf", "signature",
        ),
        "problem": (
            "Empresas gastam tempo com documentos, formulários, "
            "aprovações e processos repetitivos."
        ),
        "solution": (
            "Transformar o projeto em SaaS de documentos, "
            "workflows e automação administrativa."
        ),
        "target": "Empresas, escritórios e equipes administrativas",
        "business_model": "SaaS B2B por usuário ou volume",
        "pricing": "R$ 39 a R$ 299/mês",
        "market_problem": 17,
        "monetization": 17,
        "recurrence": 14,
        "competition": 6,
        "commercial_ease": 4,
        "differentiation": 4,
        "white_label": True,
        "api": True,
    },
    {
        "slug": "ai",
        "name": "IA e Automação",
        "keywords": (
            "ai agent", "agents", "artificial intelligence",
            "llm", "automation", "automated",
            "copilot", "assistant", "rag",
        ),
        "problem": (
            "Empresas querem automatizar tarefas e incorporar IA "
            "sem construir toda a infraestrutura do zero."
        ),
        "solution": (
            "Empacotar o projeto como serviço hospedado, API "
            "ou SaaS especializado em uma tarefa."
        ),
        "target": "Empresas e profissionais que buscam automação com IA",
        "business_model": "SaaS/API por assinatura e consumo",
        "pricing": "R$ 49 a R$ 499/mês + consumo",
        "market_problem": 16,
        "monetization": 17,
        "recurrence": 13,
        "competition": 4,
        "commercial_ease": 3,
        "differentiation": 4,
        "white_label": False,
        "api": True,
    },
]


GENERIC_RULE = {
    "slug": "generic",
    "name": "Software / SaaS B2B",
    "keywords": (),
    "problem": (
        "O projeto resolve uma necessidade de software, "
        "mas o nicho comercial ainda não foi identificado com segurança."
    ),
    "solution": (
        "Investigar um segmento específico em que o projeto possa "
        "ser oferecido como serviço hospedado."
    ),
    "target": "Empresas ou profissionais a definir",
    "business_model": "SaaS ou serviço gerenciado",
    "pricing": "Preço a validar",
    "market_problem": 8,
    "monetization": 8,
    "recurrence": 7,
    "competition": 3,
    "commercial_ease": 2,
    "differentiation": 2,
    "white_label": False,
    "api": False,
}


PERMISSIVE_LICENSES = {
    "MIT",
    "APACHE-2.0",
    "BSD-2-CLAUSE",
    "BSD-3-CLAUSE",
    "ISC",
    "UNLICENSE",
}

MEDIUM_LICENSES = {
    "MPL-2.0",
    "EPL-2.0",
    "LGPL-2.1",
    "LGPL-3.0",
}

COPYLEFT_LICENSES = {
    "GPL-2.0",
    "GPL-3.0",
}

STRONG_COPYLEFT_LICENSES = {
    "AGPL-3.0",
}



PRIMARY_SIGNALS = {
    "agro": (
        "farm management",
        "agriculture management",
        "livestock management",
        "farm software",
        "farming software",
    ),
    "health": (
        "clinic management",
        "hospital management",
        "medical management",
        "patient management",
        "healthcare platform",
        "dental management",
    ),
    "fitness": (
        "gym management",
        "fitness management",
        "personal trainer",
        "workout platform",
    ),
    "property": (
        "property management",
        "real estate management",
        "rental management",
        "tenant management",
    ),
    "booking": (
        "booking system",
        "appointment system",
        "reservation system",
        "scheduling platform",
    ),
    "crm": (
        "crm",
        "sales crm",
        "sales os",
        "sales platform",
        "customer relationship",
    ),
    "erp": (
        "erp",
        "business management",
        "enterprise resource",
        "business management platform",
    ),
    "ecommerce": (
        "ecommerce platform",
        "e-commerce platform",
        "online store",
        "marketplace platform",
        "retail management",
    ),
    "finance": (
        "finance platform",
        "financial platform",
        "fintech",
        "accounting platform",
        "billing platform",
    ),
    "education": (
        "learning management",
        "education platform",
        "school management",
        "lms",
    ),
    "documents": (
        "document management",
        "workflow platform",
        "form builder",
        "document workflow",
    ),
    "ai": (
        "ai agent",
        "ai agents",
        "llm platform",
        "rag platform",
        "ai assistant",
        "artificial intelligence platform",
    ),
}


BUSINESS_CATEGORY_SLUGS = {
    "agro",
    "health",
    "fitness",
    "property",
    "booking",
    "crm",
    "erp",
    "ecommerce",
    "finance",
    "education",
    "documents",
}


def _normalize(value):
    value = (value or "").lower()

    for char in ("-", "_", "/", ".", ",", "(", ")", "[", "]"):
        value = value.replace(char, " ")

    return " ".join(value.split())


def repository_sources(repository):
    topics = repository.topics or []

    if not isinstance(topics, list):
        topics = []

    return {
        "name": _normalize(
            f"{repository.name or ''} {repository.full_name or ''}"
        ),
        "description": _normalize(
            repository.description or ""
        ),
        "topics": [
            _normalize(str(topic))
            for topic in topics
        ],
    }


def repository_text(repository):
    sources = repository_sources(repository)

    return " ".join(
        [
            sources["name"],
            sources["description"],
            " ".join(sources["topics"]),
        ]
    )


def _rule_match_score(rule, sources):
    score = 0
    matched = set()

    name = sources["name"]
    description = sources["description"]
    topics = sources["topics"]

    topic_points = 0

    for raw_keyword in rule["keywords"]:
        keyword = _normalize(raw_keyword)

        if not keyword:
            continue

        found = False

        if keyword in name:
            score += 7
            found = True

        if keyword in description:
            score += 5
            found = True

        if any(keyword in topic for topic in topics):
            topic_points += 2
            found = True

        if found:
            matched.add(raw_keyword)

    # Evita categorias com dezenas de tópicos dominarem
    # apenas pela quantidade de tags.
    score += min(topic_points, 8)

    for raw_signal in PRIMARY_SIGNALS.get(
        rule["slug"],
        (),
    ):
        signal = _normalize(raw_signal)

        if signal in name:
            score += 12

        elif signal in description:
            score += 10

        elif any(signal in topic for topic in topics):
            score += 4

    return score, sorted(matched)


def category_rankings(repository):
    sources = repository_sources(repository)

    rankings = []

    for rule in CATEGORY_RULES:
        score, matched = _rule_match_score(
            rule,
            sources,
        )

        rankings.append(
            {
                "rule": rule,
                "score": score,
                "matched_keywords": matched,
            }
        )

    rankings.sort(
        key=lambda item: (
            item["score"],
            len(item["matched_keywords"]),
        ),
        reverse=True,
    )

    return rankings


def choose_category(repository):
    rankings = category_rankings(repository)

    if not rankings:
        return GENERIC_RULE, []

    winner = rankings[0]

    # IA deve ser tratada como tecnologia secundária quando
    # existe um negócio vertical claramente identificado.
    if winner["rule"]["slug"] == "ai":
        business_candidates = [
            item
            for item in rankings
            if (
                item["rule"]["slug"]
                in BUSINESS_CATEGORY_SLUGS
                and item["score"] >= 12
            )
        ]

        if business_candidates:
            winner = business_candidates[0]

    if winner["score"] < 5:
        return GENERIC_RULE, []

    return (
        winner["rule"],
        winner["matched_keywords"],
    )



def calculate_license_score(spdx):
    value = (spdx or "").strip().upper()

    if value in PERMISSIVE_LICENSES:
        return 5

    if value in MEDIUM_LICENSES:
        return 3

    if value in COPYLEFT_LICENSES:
        return 2

    if value in STRONG_COPYLEFT_LICENSES:
        return 1

    return 0


def license_assessment(spdx):
    value = (spdx or "").strip().upper()

    if value in PERMISSIVE_LICENSES:
        return (
            "Licença permissiva. "
            "Ainda é necessário cumprir avisos e condições da licença."
        )

    if value in MEDIUM_LICENSES:
        return (
            "Licença com obrigações específicas. "
            "Revisar requisitos antes de comercializar modificações."
        )

    if value in COPYLEFT_LICENSES:
        return (
            "Licença copyleft. "
            "Revisar cuidadosamente as obrigações de distribuição "
            "e disponibilização de código."
        )

    if value in STRONG_COPYLEFT_LICENSES:
        return (
            "Licença AGPL/copy-left forte. "
            "Uma oferta hospedada pode gerar obrigações de disponibilização "
            "do código modificado. Revisão jurídica recomendada."
        )

    return (
        "Licença não identificada ou não reconhecida. "
        "Não assumir direito de uso comercial antes de verificar "
        "a licença do projeto."
    )


def calculate_growth_score(repository):
    snapshots = repository.snapshots.order_by("captured_at")

    last = snapshots.last()

    if not last:
        return 2, 0.0

    cutoff = timezone.now() - timedelta(days=30)

    first = (
        snapshots.filter(captured_at__gte=cutoff).first()
        or snapshots.first()
    )

    if not first or first.pk == last.pk:
        return 2, 0.0

    start = max(first.stars, 1)
    growth_pct = ((last.stars - first.stars) / start) * 100

    if growth_pct >= 100:
        score = 10
    elif growth_pct >= 50:
        score = 9
    elif growth_pct >= 25:
        score = 8
    elif growth_pct >= 10:
        score = 7
    elif growth_pct >= 5:
        score = 6
    elif growth_pct > 0:
        score = 5
    elif growth_pct == 0:
        score = 2
    else:
        score = 0

    return score, round(growth_pct, 2)


def calculate_technical_maturity(repository):
    score = 0

    stars = repository.stars or 0
    forks = repository.forks or 0

    if stars >= 10000:
        score += 6
    elif stars >= 2000:
        score += 5
    elif stars >= 500:
        score += 4
    elif stars >= 100:
        score += 3
    elif stars >= 20:
        score += 2
    elif stars >= 5:
        score += 1

    if forks >= 100:
        score += 2
    elif forks >= 20:
        score += 1

    if repository.pushed_at_github:
        age = timezone.now() - repository.pushed_at_github

        if age <= timedelta(days=30):
            score += 2
        elif age <= timedelta(days=90):
            score += 1

    return min(score, 10)



def score_dimensions_from_values(scores):
    commercial_points = (
        scores["market_problem"]
        + scores["monetization"]
        + scores["recurrence"]
        + scores["competition"]
        + scores["commercial_ease"]
        + scores["license"]
        + scores["differentiation"]
    )

    technical_points = (
        scores["growth"]
        + scores["technical_maturity"]
    )

    commercial_score = round(
        (commercial_points / 80) * 100
    )

    technical_score = round(
        (technical_points / 20) * 100
    )

    return {
        "commercial_score": min(
            100,
            commercial_score,
        ),
        "technical_score": min(
            100,
            technical_score,
        ),
    }


def score_dimensions(score):
    return score_dimensions_from_values(
        {
            "market_problem": score.market_problem,
            "monetization": score.monetization,
            "recurrence": score.recurrence,
            "growth": score.growth,
            "technical_maturity": score.technical_maturity,
            "competition": score.competition,
            "commercial_ease": score.commercial_ease,
            "license": score.license,
            "differentiation": score.differentiation,
        }
    )


def evaluate_repository(repository):
    rule, matched_keywords = choose_category(
        repository
    )

    rankings = category_rankings(
        repository
    )

    text = repository_text(
        repository
    )

    market_problem = rule["market_problem"]

    if len(matched_keywords) >= 3:
        market_problem += 2

    elif len(matched_keywords) >= 2:
        market_problem += 1

    market_problem = min(
        market_problem,
        20,
    )

    monetization = rule["monetization"]

    paid_signals = (
        "subscription",
        "billing",
        "payment",
        "multi tenant",
        "saas",
        "pricing",
    )

    if any(
        signal in text
        for signal in paid_signals
    ):
        monetization = min(
            20,
            monetization + 1,
        )

    recurrence = min(
        rule["recurrence"],
        15,
    )

    growth, growth_pct = (
        calculate_growth_score(
            repository
        )
    )

    technical_maturity = (
        calculate_technical_maturity(
            repository
        )
    )

    license_score = calculate_license_score(
        repository.license_spdx
    )

    commercial_ease = min(
        rule["commercial_ease"],
        5,
    )

    # Licença desconhecida ou muito restritiva aumenta
    # a dificuldade comercial.
    if license_score == 0:
        commercial_ease = max(
            0,
            commercial_ease - 2,
        )

    elif license_score == 1:
        commercial_ease = max(
            0,
            commercial_ease - 1,
        )

    differentiation = rule["differentiation"]

    if len(matched_keywords) >= 3:
        differentiation += 1

    differentiation = min(
        differentiation,
        5,
    )

    scores = {
        "market_problem": market_problem,
        "monetization": monetization,
        "recurrence": recurrence,
        "growth": growth,
        "technical_maturity": technical_maturity,
        "competition": min(
            rule["competition"],
            10,
        ),
        "commercial_ease": commercial_ease,
        "license": license_score,
        "differentiation": differentiation,
    }

    final_score = min(
        100,
        sum(scores.values()),
    )

    dimensions = score_dimensions_from_values(
        scores
    )

    primary_slug = rule["slug"]

    secondary = []

    for item in rankings:
        secondary_rule = item["rule"]

        if secondary_rule["slug"] == primary_slug:
            continue

        if item["score"] < 5:
            continue

        secondary.append(
            secondary_rule["name"]
        )

        if len(secondary) == 2:
            break

    matched = (
        ", ".join(matched_keywords[:8])
        or "nenhuma palavra-chave forte"
    )

    secondary_text = (
        ", ".join(secondary)
        if secondary
        else "nenhuma categoria secundária relevante"
    )

    license_text = license_assessment(
        repository.license_spdx
    )

    rationale = (
        "Análise automática SaaS Hunter 0.3.1. "
        f"Nicho principal: {rule['name']}. "
        f"Categorias secundárias: {secondary_text}. "
        f"Sinais encontrados: {matched}. "
        f"Estrelas: {repository.stars}. "
        f"Forks: {repository.forks}. "
        f"Licença: {repository.license_spdx or 'não identificada'}. "
        f"{license_text} "
        f"Crescimento observado: {growth_pct}%. "
        f"Potencial comercial normalizado: "
        f"{dimensions['commercial_score']}/100. "
        f"Força técnica/momento: "
        f"{dimensions['technical_score']}/100. "
        "O score é um filtro inicial e exige validação real "
        "de mercado antes de qualquer investimento."
    )

    commercial_summary = (
        f"O projeto {repository.full_name} apresenta sinais de aplicação "
        f"no mercado de {rule['name']}. "
        f"O modelo inicial sugerido é {rule['business_model']}. "
        "Tecnologias ou categorias secundárias não substituem "
        "a classificação do problema de negócio principal. "
        "Antes de desenvolver, concorrência, demanda, licença "
        "e disposição a pagar devem ser validadas."
    )

    return {
        "rule": rule,
        "matched_keywords": matched_keywords,
        "secondary_categories": secondary,
        "scores": scores,
        "final_score": final_score,
        "commercial_score": dimensions[
            "commercial_score"
        ],
        "technical_score": dimensions[
            "technical_score"
        ],
        "growth_pct": growth_pct,
        "rationale": rationale,
        "commercial_summary": commercial_summary,
        "eligible": (
            final_score
            >= MIN_OPPORTUNITY_SCORE
        ),
    }


def save_repository_analysis(repository):
    result = evaluate_repository(repository)

    try:
        opportunity = repository.opportunity
        created = False
    except Opportunity.DoesNotExist:
        opportunity = None
        created = True

    if not result["eligible"] and opportunity is None:
        return None, False, result

    rule = result["rule"]

    defaults = {
        "problem": rule["problem"],
        "solution": rule["solution"],
        "target_customer": rule["target"],
        "market_segment": rule["name"],
        "business_model": rule["business_model"],
        "suggested_pricing": rule["pricing"],
        "commercial_summary": result["commercial_summary"],
        "saas_possible": True,
        "white_label_possible": rule["white_label"],
        "api_possible": rule["api"],
    }

    if opportunity is None:
        if result["final_score"] >= 80:
            defaults["status"] = Opportunity.Status.INVESTIGATE
        elif result["final_score"] >= 70:
            defaults["status"] = Opportunity.Status.WATCH
        else:
            defaults["status"] = Opportunity.Status.NEW

        opportunity = Opportunity.objects.create(
            repository=repository,
            **defaults,
        )

        created = True

    else:
        for field, value in defaults.items():
            setattr(opportunity, field, value)

        opportunity.save()

        created = False

    try:
        score = opportunity.score
    except OpportunityScore.DoesNotExist:
        score = OpportunityScore(
            opportunity=opportunity
        )

    for field, value in result["scores"].items():
        setattr(score, field, value)

    score.rationale = result["rationale"]

    # save() recalcula final_score no model
    score.save()

    result["final_score"] = score.final_score

    return opportunity, created, result
