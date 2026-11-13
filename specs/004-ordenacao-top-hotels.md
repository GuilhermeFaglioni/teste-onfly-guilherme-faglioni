# SPEC-004 — top_hotels ordenado por total desc, hotel_id asc

- **Status:** done
- **Issue:** [#4](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/4)
- **Autor:** orquestrador
- **Implementador / Revisor:** subagent implementador / subagent revisor
- **Origem:** test_top_hotels: ['H04','H03','H02'] vs ['H01','H02','H03']

## 1. Contexto e problema
README › Ordenação: `top_hotels` por `total_brl` decrescente, empate `hotel_id` ascendente. `src/onfly_report/services/report_builder.py:91` ordena `(amount, hotel_id)` ascendente.

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
- `tests/test_regression_report.py::test_regression_report_on_sample` — PASS → PASS (já passa desde a SPEC-003: o teste só verifica `summary`)

## 6. Novos testes propostos (escritos ANTES do código — RED)
| Arquivo::teste | Cenário | Resultado esperado | Falha esperada antes da correção |
|-|-|-|-|
| `test_top_hotels_extra.py::test_tie_breaks_by_hotel_id_asc` | H01 e H02 empatados + H03 com total menor | ['H01','H02','H03'] | ['H03','H01','H02'] (valor em ordem crescente; ajustado na implementação: só com H01/H02 não haveria RED) |
| `test_top_hotels_extra.py::test_limit_keeps_highest` | 3 hotéis, `--top 1` | só o de maior total | traz o menor |
| `test_top_hotels_extra.py::test_fewer_hotels_than_top` | 2 hotéis (H01=200, H02=300), `--top 5` | 2 itens na ordem ['H02','H01'] | ordem invertida ['H01','H02'] |

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
_Execução original. `test_fewer_hotels_than_top` passava aqui porque comparava a lista ordenada; após a revisão passou a verificar a ordem e o RED dele está em "Ajuste pós-revisão"._
```
$ pytest -q tests/test_top_hotels_extra.py tests/test_top_hotels.py
FAILED tests/test_top_hotels_extra.py::test_tie_breaks_by_hotel_id_asc
E       AssertionError: assert ['H03', 'H01', 'H02'] == ['H01', 'H02', 'H03']
FAILED tests/test_top_hotels_extra.py::test_limit_keeps_highest
E       AssertionError: assert ['H03'] == ['H02']
FAILED tests/test_top_hotels.py::test_top_hotels_are_ranked_descending
E       AssertionError: assert ['H04', 'H03', 'H02'] == ['H01', 'H02', 'H03']
3 failed, 1 passed   (test_fewer_hotels_than_top passa já, como previsto)
Obs.: no teste de empate foi incluído um 3º hotel (H03, menor total) para que o RED
reproduza; só com H01/H02 empatados a ordenação ascendente já coincidiria.
```
### GREEN
```
Mudança: report_builder.py:91 key=(item[1]["amount"], item[0]) -> (-item[1]["amount"], item[0])
$ pytest -q
26 passed in 0.60s
$ ruff check src tests
All checks passed!
$ CLI na amostra (data/exemplo-validacao.csv) -> top_hotels:
H01 1200.00 | H02 1084.00 | H12 1000.00 | H10 900.00 | H09 882.00  (confere com a tabela do README)
```
### Revisão
**VEREDITO: APROVADO** (subagent revisor).
- Diff restrito a `report_builder.py:91`, `tests/test_top_hotels_extra.py` e esta spec; nenhum arquivo proibido alterado.
- RED comprovado (2 novos + `test_top_hotels` fornecido); GREEN: `pytest -q` 26 passed (100%), ruff limpo.
- Amostra: summary, `by_month` e `top_hotels` (H01, H02, H12, H10, H09) batem integralmente com o README. Dataset completo: exit 0 (`total_reservations` 200 até a SPEC-005).
- Desvio do teste de empate validado: trava valor desc + `hotel_id` asc e pegaria uma correção ingênua com `reverse=True`. Tabela da seção 6 atualizada pelo orquestrador.
- Apontamento 2 do revisor aplicado (ver Ajuste pós-revisão)

### Ajuste pós-revisão
`test_fewer_hotels_than_top` passou a verificar a ordem: `assert _ids(report) == ["H02", "H01"]`.
```
# RED (chave antiga (item[1]["amount"], item[0]) aplicada temporariamente)
$ pytest -q tests/test_top_hotels_extra.py::test_fewer_hotels_than_top
E       AssertionError: assert ['H01', 'H02'] == ['H02', 'H01']
1 failed in 0.06s

# GREEN (chave (-item[1]["amount"], item[0]) restaurada)
$ pytest -q tests/test_top_hotels_extra.py::test_fewer_hotels_than_top
1 passed in 0.05s
$ git diff --stat src
(vazio: src idêntico ao HEAD)
$ pytest -q
26 passed in 0.65s
$ ruff check src tests
All checks passed!
```
