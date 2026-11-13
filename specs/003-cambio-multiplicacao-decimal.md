# SPEC-003 — Câmbio: amount * rate em Decimal

- **Status:** done
- **Issue:** [#3](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/3)
- **Autor:** orquestrador
- **Implementador / Revisor:** subagent implementador / subagent revisor
- **Origem:** test_currency: total_amount_brl 118.45 vs 642.00

## 1. Contexto e problema
README › Câmbio e Exatidão: converter com `amount * rate_to_brl`, Decimal, nunca float. `src/onfly_report/services/currency_converter.py:11` faz `Decimal(str(float(amount) / float(rate)))`.

## 2. Escopo
- **Dentro:** `src/onfly_report/services/currency_converter.py`
- **Fora:** leitura de taxas (`csv_rate_repository`, já Decimal); tratamento de moeda ausente (fora: README garante taxa para todas)

## 3. Causa raiz
Divide pela taxa em vez de multiplicar e passa por float, perdendo exatidão.

## 4. Plano de implementação
1. Escrever `tests/test_currency_extra.py` e provar RED.
2. Trocar para `return amount * rates[currency]`.
3. Rodar suíte completa.

## 5. Testes existentes (imutáveis) que devem passar
- `tests/test_currency.py::test_currency_conversion_to_brl` — FAIL → PASS
- `tests/test_regression_report.py::test_regression_report_on_sample` — FAIL → PASS (previsão original "até 004" corrigida: o teste só verifica `summary`, cujo último defeito era o câmbio)

## 6. Novos testes propostos (escritos ANTES do código — RED)
| Arquivo::teste | Cenário | Resultado esperado | Falha esperada antes da correção |
|-|-|-|-|
| `test_currency_extra.py::test_usd_multiplies` | 100 USD, taxa 5.42 | Decimal('542.00') | 18.45… |
| `test_currency_extra.py::test_brl_identity` | 100 BRL, taxa 1 | Decimal('100.00') | passa já |
| `test_currency_extra.py::test_exact_decimal` | 0.10 USD, taxa 5.420001 | `== Decimal('0.10') * Decimal('5.420001')` exato e tipo Decimal | divisão/float |

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
$ pytest -q tests/test_currency_extra.py
FAILED tests/test_currency_extra.py::test_usd_multiplies - AssertionError: as...
FAILED tests/test_currency_extra.py::test_exact_decimal - AssertionError: ass...
2 failed, 1 passed in 0.02s
```
### GREEN
```
$ ruff check src tests && pytest -q
All checks passed!
E         Use -v to get more diff

tests/test_top_hotels.py:18: AssertionError
=========================== short test summary info ============================
FAILED tests/test_top_hotels.py::test_top_hotels_are_ranked_descending - Asse...
1 failed, 22 passed in 0.50s
```
(test_currency e test_regression_report passam; resta só test_top_hotels, SPEC-004.)
### Revisão
**VEREDITO: APROVADO** (subagent revisor).
- Diff restrito a `currency_converter.py`, `tests/test_currency_extra.py` e esta spec; nenhum `float` restante em `src/`.
- RED comprovado (2 falhas); GREEN: `pytest -q` 22 passed / 1 failed (`test_top_hotels`, SPEC-004), ruff limpo.
- Amostra: `total_amount_brl` 7566.00, `average_nightly_rate_brl` 270.21 e `by_month` (6684.00 / 882.00) batem com o README; ordem de `top_hotels` é da 004.
- `test_regression_report` passou antes do previsto porque só verifica `summary`; previsão da seção 5 corrigida pelo orquestrador.
