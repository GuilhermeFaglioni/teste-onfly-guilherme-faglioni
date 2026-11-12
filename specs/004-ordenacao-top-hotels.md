# SPEC-004 — top_hotels ordenado por total desc, hotel_id asc

- **Status:** approved
- **Issue:** [#4](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/4)
- **Autor:** orquestrador
- **Implementador / Revisor:** —
- **Origem:** test_top_hotels: ['H04','H03','H02'] vs ['H01','H02','H03']

## 1. Contexto e problema
README › Ordenação: `top_hotels` por `total_brl` decrescente, empate `hotel_id` ascendente. `src/onfly_report/services/report_builder.py:90` ordena `(amount, hotel_id)` ascendente.

## 2. Escopo
- **Dentro:** `src/onfly_report/services/report_builder.py` (somente a chave de ordenação de top_hotels)
- **Fora:** by_month, summary, serialização, limite `--top`

## 3. Causa raiz
A chave de ordenação usa o valor em ordem crescente, invertendo o ranking.

## 4. Plano de implementação
1. Escrever `tests/test_top_hotels_extra.py` e provar RED.
2. Trocar a chave para `(-amount, hotel_id)`.
3. Rodar suíte completa.

## 5. Testes existentes (imutáveis) que devem passar
- `tests/test_top_hotels.py::test_top_hotels_are_ranked_descending` — FAIL → PASS
- `tests/test_regression_report.py::test_regression_report_on_sample` — FAIL → PASS (se 001-003 já done)

## 6. Novos testes propostos (escritos ANTES do código — RED)
| Arquivo::teste | Cenário | Resultado esperado | Falha esperada antes da correção |
|-|-|-|-|
| `test_top_hotels_extra.py::test_tie_breaks_by_hotel_id_asc` | H02 e H01 com mesmo total | ['H01','H02'] | ordem invertida |
| `test_top_hotels_extra.py::test_limit_keeps_highest` | 3 hotéis, `--top 1` | só o de maior total | traz o menor |
| `test_top_hotels_extra.py::test_fewer_hotels_than_top` | 2 hotéis, `--top 5` | 2 itens | passa já |

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
