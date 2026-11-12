# Entrega — Consolidador de reservas

## Defeitos corrigidos
| # | Arquivo | Sintoma | Causa raiz (1 frase) | Correção | Teste |
|-|-|-|-|-|-|

## Como investiguei

## Como validar
```bash
source .venv/bin/activate
pytest -q
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
```

## Resultado do pytest
