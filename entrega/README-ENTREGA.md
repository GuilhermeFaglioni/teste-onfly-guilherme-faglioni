# Entrega — Consolidador de reservas

## Defeitos corrigidos
| # | Arquivo | Sintoma | Causa raiz (1 frase) | Correção | Teste |
|-|-|-|-|-|-|
| 1 | `src/onfly_report/services/status_policy.py` | NO_SHOW entrava em noites e valores (`test_status_rules`: 120.00 vs 100.00) | `is_billable` excluía só `CANCELLED` em vez de aceitar apenas `CONFIRMED`. | `return status == "CONFIRMED"` ([SPEC-001](../specs/001-status-faturavel.md), #1) | `tests/test_status_policy_extra.py` |
| 2 | `src/onfly_report/services/stay_calculator.py` | Noites negativas na virada de mês/ano (`test_nights`: -28 vs 3) | Subtraía o dia do mês (`checkout.day - checkin.day`) em vez da diferença entre as datas. | `(checkout - checkin).days * rooms` ([SPEC-002](../specs/002-noites-nao-inclusivas.md), #2) | `tests/test_stay_calculator_extra.py` |
| 3 | `src/onfly_report/services/currency_converter.py` | Valores em moeda estrangeira errados (`test_currency`: 118.45 vs 642.00) | Dividia pela taxa em vez de multiplicar e passava por `float`, perdendo exatidão. | `return amount * rates[currency]` em `Decimal` ([SPEC-003](../specs/003-cambio-multiplicacao-decimal.md), #3) | `tests/test_currency_extra.py` |
| 4 | `src/onfly_report/services/report_builder.py` | `top_hotels` em ordem crescente (`test_top_hotels`: ['H04','H03','H02'] vs ['H01','H02','H03']) | A chave de ordenação usava o total em ordem crescente, invertendo o ranking. | chave `(-total, hotel_id)` ([SPEC-004](../specs/004-ordenacao-top-hotels.md), #4) | `tests/test_top_hotels_extra.py` |
| 5 | `src/onfly_report/repositories/csv_reservation_repository.py` | Dataset real (300 reservas) consolidado com só 200; nenhum teste fornecido detectava | Um corte fixo (`if len(rows) == 200: break`) descartava silenciosamente as linhas após a 200ª. | Remoção do corte ([SPEC-005](../specs/005-leitura-sem-limite-linhas.md), #5) | `tests/test_reservation_repository_extra.py` |
| — | (testes adicionais) | Contrato da CLI e exatidão sem cobertura nos testes fornecidos | Não é defeito: lacuna de cobertura (exit codes, `--top`, half-up após a soma, mês do check-in, amostra do README). | 9 testes novos, RED por mutação ([SPEC-006](../specs/006-testes-contrato-cli.md), #6) | `tests/test_cli_contract_extra.py` |

## Como investiguei

Trabalhei com **SDD + TDD** e um fluxo de agentes, descrito em `CLAUDE.md`: a sessão principal orquestra e os subagents investigam, implementam e revisam. O uso de IA está declarado em `uso-de-ia/declaracao.md`.

1. **Leitura do enunciado:** o `README.md` é a fonte da verdade. Extraí as regras de negócio e o contrato da CLI. O contrato do JSON está documentado em `docs/SCHEMA.md` e é protegido por `tests/test_schema_contract.py`.
2. **Linha de base:** rodei `pytest -q` antes de qualquer correção: os 5 testes fornecidos falhavam e os 5 testes de schema passavam.
3. **Investigação:** usei 3 investigadores somente leitura em paralelo, cada um com um escopo:
   - leitura dos CSVs e conversão de tipos;
   - regras de cálculo;
   - montagem do relatório e CLI.

   Cada achado veio com `arquivo:linha`, a regra violada e a evidência. Os achados foram tratados como hipótese até haver um teste RED. Assim apareceu o defeito 5 (corte em 200 linhas), que nenhum teste fornecido detectava, e também as lacunas de cobertura que viraram a SPEC-006.
4. **Especificação:** escrevi uma spec por defeito em `specs/`, com escopo, causa raiz, plano, testes imutáveis esperados, testes novos com a falha esperada e Definition of Done. Cada spec tem uma issue no GitHub (#1 a #6) e está registrada em `specs/README.md`.
5. **Implementação (TDD):** para cada spec, o implementador:
   - escreveu os testes novos e comprovou o **RED**;
   - aplicou a mudança mínima até o **GREEN**;
   - registrou as saídas na própria spec.

   Na SPEC-006, que cobre comportamento já correto, o RED foi comprovado **por mutação**: o código foi quebrado temporariamente e depois revertido.
6. **Revisão:** um revisor somente leitura conferiu, para cada spec:
   - o escopo do diff e os arquivos protegidos;
   - o RED antes do GREEN e o DoD;
   - a amostra do README.

   Na SPEC-005, ele recalculou o dataset completo de forma independente da CLI.
7. **Integração:** a CI (`.github/workflows/ci.yml`) bloqueia alterações em testes ou dados protegidos, exige spec quando `src/` muda e roda ruff, o teste de schema, a suíte e a CLI. Cada spec foi para `main` num PR próprio (#7 a #12) e passou por code review humano antes do merge.

## Como validar
```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
ruff check src tests
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

**Amostra (`exemplo-validacao.csv`):**
- O relatório bate integralmente com as tabelas do README: summary 12/9/2/1, 28 noites, 7566.00 e média 270.21; `by_month`; `top_hotels` na ordem H01, H02, H12, H10, H09.
- Essa comparação está automatizada em `tests/test_cli_contract_extra.py::test_validation_sample_matches_readme`.

**Dataset completo (`reservas_hoteis.csv`, exit 0):**

| Campo | Valor |
|-|-|
| `total_reservations` | 300 |
| `confirmed_reservations` | 235 |
| `cancelled_reservations` | 31 |
| `no_show_reservations` | 34 |
| `total_room_nights` | 1347 |
| `total_amount_brl` | 396170.00 |
| `average_nightly_rate_brl` | 294.11 |

Esses valores foram conferidos por um cálculo independente (csv mais `Decimal`, sem o código da CLI).

**Integridade:** os testes fornecidos, os arquivos `data/reservas_hoteis.csv` e `data/taxas_cambio.csv` e o `README.md` estão idênticos ao commit original (`367b127`).

## Resultado do pytest
Python 3.11.18:
```
$ pytest -q
.....................................                                    [100%]
37 passed in 1.01s

$ ruff check src tests
All checks passed!
```
- 5 testes fornecidos (todos passam, sem alteração);
- 5 testes de contrato de schema;
- 27 testes adicionais criados pelas specs 001 a 006.
