# SPEC-005 — Ler todas as reservas do CSV

- **Status:** done
- **Issue:** [#5](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/5)
- **Autor:** orquestrador
- **Implementador / Revisor:** subagent implementador / subagent revisor
- **Origem:** nenhum teste fornecido; dataset real tem 300 reservas e o relatório usa 200

## 1. Contexto e problema
README › Totais: `total_reservations` = número de reservas no arquivo. `src/onfly_report/repositories/csv_reservation_repository.py:47` interrompe a leitura em 200 linhas.

## 2. Escopo
- **Dentro:** `src/onfly_report/repositories/csv_reservation_repository.py`
- **Fora:** validação de colunas e erros de leitura

## 3. Causa raiz
Um corte fixo (`if len(rows) == 200: break`) descarta silenciosamente todas as linhas após a 200ª.

## 4. Plano de implementação
1. Escrever `tests/test_reservation_repository_extra.py` e provar RED.
2. Remover o corte.
3. Rodar suíte completa e CLI no dataset (`total_reservations` = 300).

## 5. Testes existentes (imutáveis) que devem passar
- Todos os testes fornecidos — sem regressão

## 6. Novos testes propostos (escritos ANTES do código — RED)
| Arquivo::teste | Cenário | Resultado esperado | Falha esperada antes da correção |
|-|-|-|-|
| `test_reservation_repository_extra.py::test_reads_more_than_200_rows` | CLI com 250 reservas | total_reservations 250 | 200 |
| `test_reservation_repository_extra.py::test_real_dataset_count` | `data/reservas_hoteis.csv` lido pelo `CsvReservationRepository` | 300 linhas (`len(read())`) | 200 |

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
$ pytest -q tests/test_reservation_repository_extra.py
E       assert 200 == 250
E       AssertionError: assert 200 == 300
FAILED tests/test_reservation_repository_extra.py::test_reads_more_than_200_rows
FAILED tests/test_reservation_repository_extra.py::test_real_dataset_count - ...
2 failed in 0.08s
```
### GREEN
```
$ pytest -q tests/test_reservation_repository_extra.py
2 passed in 0.05s
$ pytest -q
28 passed in 0.64s
$ ruff check src tests
All checks passed!
$ PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output <tmp>/r.json
Reservas: 300 | Confirmadas: 235 | Noites: 1347 | Total BRL: 396170.00   (exit 0)
summary: total_reservations 300, confirmed 235, cancelled 31, no_show 34, total_room_nights 1347, total_amount_brl "396170.00", average_nightly_rate_brl "294.11"
```
### Revisão
**VEREDITO: APROVADO** (subagent revisor).
- Diff restrito à remoção do corte em `csv_reservation_repository.py`, `tests/test_reservation_repository_extra.py` e esta spec; `data/` intacto.
- Nenhum outro corte de leitura em `src/` (único `[:` é o limite legítimo de `--top`).
- RED comprovado (200 == 250, 200 == 300); GREEN: `pytest -q` 28 passed, ruff limpo.
- Dataset completo conferido com cálculo independente (csv + Decimal, sem o código da CLI): 300 / 235 / 31 / 34, 1347 noites, 396170.00, média 294.11 — idêntico à CLI.
- Amostra do README continua batendo integralmente.
- Observação de baixa severidade (descrição de `test_real_dataset_count` na seção 6) ajustada pelo orquestrador.
