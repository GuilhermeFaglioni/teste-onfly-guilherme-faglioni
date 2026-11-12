# SPEC-002 — Noites pela diferença de datas

- **Status:** done
- **Issue:** [#2](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/2)
- **Autor:** orquestrador
- **Implementador / Revisor:** subagent implementador (general-purpose) / subagent revisor (general-purpose)
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
$ pytest -q tests/test_stay_calculator_extra.py
E       assert -27 == 2
E        +  where -27 = calculate_room_nights(datetime.date(2024, 2, 28), datetime.date(2024, 3, 1), 1)
E        +    where datetime.date(2024, 2, 28) = date(2024, 2, 28)
E        +    and   datetime.date(2024, 3, 1) = date(2024, 3, 1)

tests/test_stay_calculator_extra.py:25: AssertionError
=========================== short test summary info ============================
FAILED tests/test_stay_calculator_extra.py::test_month_boundary - assert -28 ...
FAILED tests/test_stay_calculator_extra.py::test_year_boundary - assert -29 == 2
FAILED tests/test_stay_calculator_extra.py::test_multiple_rooms_across_month
FAILED tests/test_stay_calculator_extra.py::test_leap_february - assert -27 == 2
4 failed, 1 passed in 0.03s
```
### GREEN
```
$ pytest -q && ruff check src tests
E         Use -v to get more diff

tests/test_top_hotels.py:18: AssertionError
=========================== short test summary info ============================
FAILED tests/test_currency.py::test_currency_conversion_to_brl - AssertionErr...
FAILED tests/test_regression_report.py::test_regression_report_on_sample - As...
FAILED tests/test_top_hotels.py::test_top_hotels_are_ranked_descending - Asse...
3 failed, 17 passed in 0.68s
All checks passed!
# falhas restantes: specs 003/004 (fora do escopo)
```
### Revisão
**VEREDITO: APROVADO** (subagent revisor).
- Diff restrito a `stay_calculator.py`, `tests/test_stay_calculator_extra.py` e esta spec; nenhum arquivo proibido alterado.
- RED comprovado (4 falhas: -28, -29, -56, -27); GREEN: `pytest -q` 17 passed / 3 failed (specs 003-004), ruff limpo.
- Amostra: `total_room_nights` 28 e `by_month` 25/3 batem com o README; valores BRL e ranking dependem de 003-004.
- Apontamentos de baixa severidade (status e campo Revisor) resolvidos pelo orquestrador.
