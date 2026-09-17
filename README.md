# SaaS Hunter - versão pronta

Pasta oficial local:
`/home/carlosjs/SaaS/SaaS_Hunter`

## O que já está pronto

- Django
- PostgreSQL 16
- Redis
- Celery Worker
- Celery Beat
- Scanner inicial do GitHub
- Dashboard
- Admin automático via `.env`
- Rede Docker explícita
- Espera automática pelo banco antes do Django iniciar
- Porta local: `8020`
- Domínio futuro: `hunter.confronta.com.br`

## Instalação

1. Extraia o conteúdo desta pasta em:

```bash
/home/carlosjs/SaaS/SaaS_Hunter
```

2. Crie o `.env`:

```bash
cp .env.example .env
nano .env
```

3. Altere pelo menos:

```env
DJANGO_SECRET_KEY=uma-chave-forte
POSTGRES_PASSWORD=uma-senha-forte
ADMIN_USERNAME=carlos
ADMIN_EMAIL=
ADMIN_PASSWORD=sua-senha-de-login
GITHUB_TOKEN=
```

4. Suba:

```bash
docker compose down --remove-orphans
docker compose up -d --build
```

5. Confira:

```bash
docker compose ps
```

6. Acesse:

- http://localhost:8020/
- http://localhost:8020/admin/
- http://localhost:8020/health/

Login:
- usuário: valor de `ADMIN_USERNAME`
- senha: valor de `ADMIN_PASSWORD`


## Instalação simplificada

Depois de extrair na pasta oficial:

```bash
cd /home/carlosjs/SaaS/SaaS_Hunter
chmod +x install.sh
./install.sh
```

Credenciais locais iniciais:

- Usuário: `carlos`
- Senha: `Hunter@2026!Carlos`

Antes de publicar na VPS, troque a senha no `.env`.


## Motor automático de oportunidades — 0.3

O SaaS Hunter agora:

- classifica repositórios por nicho;
- identifica possíveis clientes;
- sugere modelo comercial;
- sugere faixa inicial de preço;
- calcula score de 0 a 100;
- considera licença, maturidade e crescimento;
- cria oportunidades automaticamente;
- executa nova análise após cada caça.

O score é um filtro inicial e não substitui validação real de mercado.
