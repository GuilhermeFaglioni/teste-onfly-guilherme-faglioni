# Entrega — Consolidador de reservas

## Defeitos corrigidos
| # | Arquivo | Sintoma | Causa raiz (1 frase) | Correção | Teste |
|-|-|-|-|-|-|
| 1 | `src/onfly_report/services/status_policy.py` | NO_SHOW entrava em noites e valores (`test_status_rules`: 120.00 vs 100.00) | `is_billable` excluía só `CANCELLED` em vez de aceitar apenas `CONFIRMED`. | `return status == "CONFIRMED"` ([SPEC-001](../specs/001-status-faturavel.md), #1) | `tests/test_status_policy_extra.py` |
| 2 | `src/onfly_report/services/stay_calculator.py` | Noites negativas na virada de mês/ano (`test_nights`: -28 vs 3) | Subtraía o dia do mês (`checkout.day - checkin.day`) em vez da diferença entre as datas. | `(checkout - checkin).days * rooms` ([SPEC-002](../specs/002-noites-nao-inclusivas.md), #2) | `tests/test_stay_calculator_extra.py` |
| 3 | `src/onfly_report/services/currency_converter.py` | Valores em moeda estrangeira errados (`test_currency`: 118.45 vs 642.00) | Dividia pela taxa em vez de multiplicar e passava por `float`, perdendo exatidão. | `return amount * rates[currency]` em `Decimal` ([SPEC-003](../specs/003-cambio-multiplicacao-decimal.md), #3) | `tests/test_currency_extra.py` |
| 4 | `src/onfly_report/services/report_builder.py` | `top_hotels` em ordem crescente (`test_top_hotels`: ['H04','H03','H02'] vs ['H01','H02','H03']) | A chave de ordenação usava o total em ordem crescente, invertendo o ranking. | chave `(-total, hotel_id)` ([SPEC-004](../specs/004-ordenacao-top-hotels.md), #4) | `tests/test_top_hotels_extra.py` |

## Como investiguei

## Como validar
```bash
source .venv/bin/activate
pytest -q
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
```

## Resultado do pytest
