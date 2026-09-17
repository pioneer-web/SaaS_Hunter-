#!/usr/bin/env bash
set -e

echo "=== SaaS Hunter ==="
echo "Recriando somente os containers/volumes deste projeto..."
docker compose down -v --remove-orphans || true
docker compose up -d --build

echo
echo "Status:"
docker compose ps

echo
echo "Pronto."
echo "Painel: http://localhost:8020/"
echo "Admin:  http://localhost:8020/admin/"
echo "Usuario: carlos"
echo "Senha:   Hunter@2026!Carlos"
