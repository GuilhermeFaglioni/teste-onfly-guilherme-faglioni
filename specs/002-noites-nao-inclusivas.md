# SPEC-002 — Noites pela diferença de datas

- **Status:** draft
- **Issue:** [#2](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/2)
- **Autor:** orquestrador
- **Implementador / Revisor:** —
- **Origem:** test_nights: total_room_nights -28 vs 3

## 1. Contexto e problema
README › Noites: `(checkout_date - checkin_date).days * rooms`, inclusive em virada de mês/ano. `src/onfly_report/services/stay_calculator.py:10` faz `(checkout.day - checkin.day) * rooms`.

## 2. Escopo
- **Dentro:** `src/onfly_report/services/stay_calculator.py`
- **Fora:** parsing de datas (`row_parser`, já correto)

## 3. Causa raiz
Subtrai o dia do mês em vez das datas, quebrando qualquer estadia que atravesse mês ou ano.

## 4. Plano de implementação
1. Escrever `tests/test_stay_calculator_extra.py` e provar RED.
2. Trocar para `(checkout - checkin).days * rooms`.
3. Rodar suíte completa.

## 5. Testes existentes (imutáveis) que devem passar
- `tests/test_nights.py::test_nights_across_month_boundary` — FAIL → PASS
- `tests/test_regression_report.py::test_regression_report_on_sample` — continua FAIL até 001/003/004

## 6. Novos testes propostos (escritos ANTES do código — RED)
| Arquivo::teste | Cenário | Resultado esperado | Falha esperada antes da correção |
|-|-|-|-|
| `test_stay_calculator_extra.py::test_same_month` | 10/01→13/01, 1 quarto | 3 | passa já |
| `test_stay_calculator_extra.py::test_month_boundary` | 30/01→02/02 | 3 | -28 |
| `test_stay_calculator_extra.py::test_year_boundary` | 31/12/2024→02/01/2025 | 2 | -29 |
| `test_stay_calculator_extra.py::test_multiple_rooms_across_month` | 30/01→02/02, 2 quartos | 6 | -56 |
| `test_stay_calculator_extra.py::test_leap_february` | 28/02/2024→01/03/2024 | 2 | -27 |

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
