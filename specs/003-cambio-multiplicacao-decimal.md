# SPEC-003 — Câmbio: amount * rate em Decimal

- **Status:** approved
- **Issue:** [#3](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/3)
- **Autor:** orquestrador
- **Implementador / Revisor:** —
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
- `tests/test_regression_report.py::test_regression_report_on_sample` — continua FAIL até 001/002/004

## 6. Novos testes propostos (escritos ANTES do código — RED)
| Arquivo::teste | Cenário | Resultado esperado | Falha esperada antes da correção |
|-|-|-|-|
| `test_currency_extra.py::test_usd_multiplies` | 100 USD, taxa 5.42 | Decimal('542.00') | 18.45… |
| `test_currency_extra.py::test_brl_identity` | 100 BRL, taxa 1 | Decimal('100.00') | passa já |
| `test_currency_extra.py::test_exact_decimal` | 0.10 USD, taxa 5.420001 | `== Decimal('0.10') * Decimal('5.420001')` exato e tipo Decimal | divisão/float |

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
