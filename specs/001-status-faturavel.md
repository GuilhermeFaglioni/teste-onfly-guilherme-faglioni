# SPEC-001 — Só CONFIRMED é faturável

- **Status:** done
- **Issue:** [#1](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/1)
- **Autor:** orquestrador
- **Implementador / Revisor:** subagent implementador (general-purpose) / subagent revisor (general-purpose)
- **Origem:** test_status_rules: total_amount_brl 120.00 vs 100.00

## 1. Contexto e problema
README › Status: só `CONFIRMED` é faturável; `CANCELLED` e `NO_SHOW` só entram nas contagens. `src/onfly_report/services/status_policy.py:8` retorna `status != "CANCELLED"`, faturando NO_SHOW.

## 2. Escopo
- **Dentro:** `src/onfly_report/services/status_policy.py`
- **Fora:** contagens por status no `report_builder` (já corretas); qualquer outro módulo

## 3. Causa raiz
`is_billable` usa lista de exclusão (`!= "CANCELLED"`) em vez de aceitar apenas `CONFIRMED`, então NO_SHOW e status desconhecidos são faturados.

## 4. Plano de implementação
1. Escrever `tests/test_status_policy_extra.py` e provar RED.
2. Trocar a regra para `return status == "CONFIRMED"`.
3. Rodar suíte completa.

## 5. Testes existentes (imutáveis) que devem passar
- `tests/test_status_rules.py::test_status_rules_exclude_cancelled_and_no_show` — FAIL → PASS
- `tests/test_regression_report.py::test_regression_report_on_sample` — FAIL → continua FAIL até 002-004

## 6. Novos testes propostos (escritos ANTES do código — RED)
| Arquivo::teste | Cenário | Resultado esperado | Falha esperada antes da correção |
|-|-|-|-|
| `tests/test_status_policy_extra.py::test_is_billable[CONFIRMED]` | unitário | True | passa já (não é RED) |
| `tests/test_status_policy_extra.py::test_is_billable[NO_SHOW]` | unitário | False | retorna True |
| `tests/test_status_policy_extra.py::test_is_billable[CANCELLED]` | unitário | False | passa já |
| `tests/test_status_policy_extra.py::test_is_billable[PENDING]` | status desconhecido | False | retorna True |
| `tests/test_status_policy_extra.py::test_no_show_counted_but_not_billed` | CLI: 1 CONFIRMED + 1 NO_SHOW | no_show=1, noites e valor só do CONFIRMED | valor inclui NO_SHOW |

## 7. Definition of Done
- [x] Testes novos escritos e RED comprovado (evidência abaixo)
- [x] Testes novos e imutáveis listados passam (GREEN)
- [x] `pytest -q` sem regressão (falhas restantes só as de outras specs abertas)
- [x] `ruff check src tests` limpo
- [x] `tests/test_schema_contract.py` passa; schema inalterado
- [x] Nenhum arquivo proibido alterado
- [x] Revisor: APROVADO
- [x] Linha adicionada em `entrega/README-ENTREGA.md`

## 8. Evidências
### RED
```
$ pytest -q tests/test_status_policy_extra.py
E       AssertionError: assert True is False
E        +  where True = is_billable('NO_SHOW')
E       AssertionError: assert True is False
E        +  where True = is_billable('PENDING')
E       assert 4 == 1
FAILED tests/test_status_policy_extra.py::test_is_billable[NO_SHOW] - Asserti...
FAILED tests/test_status_policy_extra.py::test_is_billable[PENDING] - Asserti...
FAILED tests/test_status_policy_extra.py::test_no_show_counted_but_not_billed
3 failed, 2 passed in 0.18s
```
### GREEN
```
$ pytest -q ; ruff check src tests ; pytest -q tests/test_schema_contract.py
FAILED tests/test_currency.py::test_currency_conversion_to_brl - AssertionErr...
FAILED tests/test_nights.py::test_nights_across_month_boundary - assert -28 == 3
FAILED tests/test_regression_report.py::test_regression_report_on_sample - As...
FAILED tests/test_top_hotels.py::test_top_hotels_are_ranked_descending - Asse...
4 failed, 11 passed in 0.58s
All checks passed!
5 passed in 0.28s
```
### Revisão
**VEREDITO: APROVADO** (subagent revisor).
- Diff restrito a `status_policy.py`, `tests/test_status_policy_extra.py` e esta spec; nenhum arquivo proibido alterado.
- RED comprovado (3 falhas: NO_SHOW, PENDING, CLI 4 == 1); GREEN: `pytest -q` 11 passed / 4 failed (specs 002-004), ruff limpo, schema 5 passed.
- Amostra: contagens batem com o README (12/9/2/1); noites e valores dependem de 002-003.
- Apontamentos de baixa severidade (campo Implementador/Revisor e esta seção) resolvidos pelo orquestrador.
