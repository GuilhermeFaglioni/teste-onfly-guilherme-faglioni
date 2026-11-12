# SPEC-006 — Testes de contrato da CLI e exatidão

- **Status:** draft
- **Issue:** [#6](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/6)
- **Autor:** orquestrador
- **Implementador / Revisor:** —
- **Origem:** comportamentos corretos hoje, mas sem teste fornecido

## 1. Contexto e problema
README › Contrato do CLI e Exatidão. O investigador verificou que estão corretos, mas sem cobertura: exit codes, validação de `--top`, half-up só na serialização, média sem noites, mês do check-in, amostra de validação.

## 2. Escopo
- **Dentro:** somente novos testes em `tests/test_cli_contract_extra.py`; `src/` só se algum teste revelar defeito (aí ESCALATE)
- **Fora:** qualquer correção de defeito de 001-005

## 3. Causa raiz
Não é defeito: lacuna de cobertura que deixaria regressões passarem.

## 4. Plano de implementação
1. Escrever os testes. Como o comportamento já está correto, o RED é demonstrado por **mutação**: alterar temporariamente o ponto do código, ver o teste falhar, reverter (registrar a saída).
2. Executar depois de 001-005 para o teste da amostra.

## 5. Testes existentes (imutáveis) que devem passar
- Todos os testes fornecidos — sem regressão

## 6. Novos testes propostos (escritos ANTES do código — RED)
| Arquivo::teste | Cenário | Resultado esperado | Falha esperada antes da correção |
|-|-|-|-|
| `test_cli_contract_extra.py::test_exit_0_and_output_created` | entrada válida | exit 0, arquivo criado | mutação |
| `test_cli_contract_extra.py::test_exit_2_missing_input` | arquivo inexistente | exit 2 | mutação |
| `test_cli_contract_extra.py::test_exit_2_invalid_top[0,-1,abc]` | `--top` inválido | exit 2 | mutação |
| `test_cli_contract_extra.py::test_exit_1_unexpected_error` | ReportBuilder.build lança (monkeypatch em `main`) | exit 1 | mutação |
| `test_cli_contract_extra.py::test_half_up_and_sum_before_round` | 3× 0.335 BRL | "1.01" (não "1.02"/"1.00") | mutação |
| `test_cli_contract_extra.py::test_by_month_uses_checkin_month` | 31/01→02/02 | só 2025-01 | mutação |
| `test_cli_contract_extra.py::test_validation_sample_matches_readme` | `data/exemplo-validacao.csv` | tabelas da amostra no README | falha até 001-005 |

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
