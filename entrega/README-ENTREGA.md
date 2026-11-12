# Entrega — Consolidador de reservas

## Defeitos corrigidos
| # | Arquivo | Sintoma | Causa raiz (1 frase) | Correção | Teste |
|-|-|-|-|-|-|
| 1 | `src/onfly_report/services/status_policy.py` | NO_SHOW entrava em noites e valores (`test_status_rules`: 120.00 vs 100.00) | `is_billable` excluía só `CANCELLED` em vez de aceitar apenas `CONFIRMED`. | `return status == "CONFIRMED"` ([SPEC-001](../specs/001-status-faturavel.md), #1) | `tests/test_status_policy_extra.py` |

## Como investiguei

## Como validar
```bash
source .venv/bin/activate
pytest -q
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
```

## Resultado do pytest
