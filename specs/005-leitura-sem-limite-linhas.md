# SPEC-005 — Ler todas as reservas do CSV

- **Status:** approved
- **Issue:** [#5](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/5)
- **Autor:** orquestrador
- **Implementador / Revisor:** —
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
| `test_reservation_repository_extra.py::test_real_dataset_count` | `data/reservas_hoteis.csv` | total_reservations 300 | 200 |

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
