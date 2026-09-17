#!/usr/bin/env bash
set -e

echo "=== SaaS Hunter ==="
echo "Atualizando aplicação..."

docker compose up -d --build

echo
echo "Status:"
docker compose ps

echo
echo "SaaS Hunter iniciado."
echo "Painel: http://localhost:8020/"
echo "Admin:  http://localhost:8020/admin/"
echo
echo "As credenciais são definidas exclusivamente no arquivo .env."
