# SPEC-001 — Só CONFIRMED é faturável

- **Status:** approved
- **Issue:** [#1](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/1)
- **Autor:** orquestrador
- **Implementador / Revisor:** —
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
- [ ] Testes novos escritos e RED comprovado (evidência abaixo)
- [ ] Testes novos e imutáveis listados passam (GREEN)
- [ ] `pytest -q` sem regressão (falhas restantes só as de outras specs abertas)
- [ ] `ruff check src tests` limpo
- [ ] `tests/test_schema_contract.py` passa; schema inalterado
- [ ] Nenhum arquivo proibido alterado
- [ ] Revisor: APROVADO
- [ ] Linha adicionada em `entrega/README-ENTREGA.md`

## 8. Evidências
### RED
```
```
### GREEN
```
```
### Revisão
