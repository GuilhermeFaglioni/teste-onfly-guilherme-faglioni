# SPEC-006 — Testes de contrato da CLI e exatidão

- **Status:** done
- **Issue:** [#6](https://github.com/GuilhermeFaglioni/teste-onfly-guilherme-faglioni/issues/6)
- **Autor:** orquestrador
- **Implementador / Revisor:** subagent implementador / subagent revisor
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
Sem mutação os 9 testes passaram (nenhum defeito real). RED por mutação (cada uma aplicada isoladamente e revertida com `git checkout -- src`; `git diff src` vazio ao final). Desvio: `--top abc` exigiu mutação própria (type=int tolerante), e half-up foi provado com 2 mutações (arredondar por linha e HALF_EVEN).

#### exit 0
```
mutação: src/onfly_report/cli.py: '    return 0
' -> '    return 3
'
E       AssertionError: 
E       assert 3 == 0
E        +  where 3 = CompletedProcess(args=['<repo>/.venv/bin/python...out/report.json'], returncode=3, stdout='Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00\n', stderr='').returncode
FAILED tests/test_cli_contract_extra.py::test_exit_0_and_output_created - Ass...
1 failed in 0.07s
```
#### exit 2 input
```
mutação: src/onfly_report/cli.py: 'err)
        return 2' -> 'err)
        return 1'
E       AssertionError: assert 1 == 2
E        +  where 1 = CompletedProcess(args=['<repo>/.venv/bin/python...hb/98s4sj0j4hdcj93vycp62_4w0000gn/T/pytest-of-guilhermefaglioni/pytest-37/test_exit_2_missing_input0/nao-existe.csv\n').returncode
FAILED tests/test_cli_contract_extra.py::test_exit_2_missing_input - Assertio...
1 failed in 0.06s
```
#### top 0/-1
```
mutação: src/onfly_report/cli.py: 'if args.top < 1:' -> 'if args.top < -5:'
E       AssertionError: assert 0 == 2
E        +  where 0 = CompletedProcess(args=['<repo>/.venv/bin/python...n', '--top', '0'], returncode=0, stdout='Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00\n', stderr='').returncode
E       AssertionError: assert 0 == 2
E        +  where 0 = CompletedProcess(args=['<repo>/.venv/bin/python...', '--top', '-1'], returncode=0, stdout='Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00\n', stderr='').returncode
FAILED tests/test_cli_contract_extra.py::test_exit_2_invalid_top[0] - Asserti...
FAILED tests/test_cli_contract_extra.py::test_exit_2_invalid_top[-1] - Assert...
2 failed, 1 passed in 0.17s
```
#### top abc
```
mutação: src/onfly_report/cli.py: 'type=int, default=5' -> 'type=lambda s: int(s) if s.lstrip("-").isdigit() else 5, default=5'
E       AssertionError: assert 0 == 2
E        +  where 0 = CompletedProcess(args=['<repo>/.venv/bin/python..., '--top', 'abc'], returncode=0, stdout='Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00\n', stderr='').returncode
FAILED tests/test_cli_contract_extra.py::test_exit_2_invalid_top[abc] - Asser...
1 failed, 2 passed in 0.18s
```
#### exit 1
```
mutação: src/onfly_report/cli.py: 'relatório")
        return 1' -> 'relatório")
        return 2'
E       assert 2 == 1
FAILED tests/test_cli_contract_extra.py::test_exit_1_unexpected_error - asser...
1 failed in 0.02s
```
#### arredonda por linha
```
mutação: src/onfly_report/services/report_builder.py: 'total_amount += amount_brl' -> 'total_amount += amount_brl.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)'
E       AssertionError: assert '1.02' == '1.01'
E         
E         - 1.01
E         ?    ^
E         + 1.02
E         ?    ^
FAILED tests/test_cli_contract_extra.py::test_half_up_and_sum_before_round - ...
1 failed in 0.06s
```
#### half-even
```
mutação: src/onfly_report/services/report_builder.py: 'rounding=ROUND_HALF_UP))' -> 'rounding="ROUND_HALF_EVEN"))'
E       AssertionError: assert '1.00' == '1.01'
E         
E         - 1.01
E         ?    ^
E         + 1.00
E         ?    ^
FAILED tests/test_cli_contract_extra.py::test_half_up_and_sum_before_round - ...
1 failed in 0.07s
```
#### mês do checkout
```
mutação: src/onfly_report/services/report_builder.py: 'row.checkin.strftime' -> 'row.checkout.strftime'
E       AssertionError: assert ['2025-02'] == ['2025-01']
E         
E         At index 0 diff: '2025-02' != '2025-01'
E         Use -v to get more diff
FAILED tests/test_cli_contract_extra.py::test_by_month_uses_checkin_month - A...
1 failed in 0.07s
```
#### amostra
```
mutação: src/onfly_report/services/report_builder.py: 'hotels[row.hotel_id]["room_nights"] += room_nights' -> 'hotels[row.hotel_id]["room_nights"] += 1'
E       AssertionError: assert [{'hotel_id':...l': '882.00'}] == [{'hotel_id':...l': '882.00'}]
E         
E         At index 0 diff: {'hotel_id': 'H01', 'hotel_name': 'Hotel Aurora Paulista', 'room_nights': 1, 'total_brl': '1200.00'} != {'hotel_id': 'H01', 'hotel_name': 'Hotel Aurora Paulista', 'room_nights': 3, 'total_brl': '1200.00'}
E         Use -v to get more diff
FAILED tests/test_cli_contract_extra.py::test_validation_sample_matches_readme
1 failed in 0.07s
```
### GREEN
```
$ pytest -q
.....................................                                    [100%]
37 passed in 0.95s
$ ruff check src tests
All checks passed!
$ git diff --stat src
(vazio)
```
### Revisão
**VEREDITO: APROVADO** (subagent revisor).
- Diff restrito a `tests/test_cli_contract_extra.py` e esta spec; `git diff HEAD -- src` vazio (nenhuma mutação esquecida); nenhum arquivo proibido alterado.
- 9 testes passam sem mutação (nenhum defeito real oculto). Revisor reproduziu 5 mutações numa cópia fora do repositório — todas derrubam os testes esperados.
- Valores fixos do teste da amostra conferidos com as tabelas do README.
- Testes determinísticos, escrevem só em `tmp_path`.
- Desvios declarados (mutação própria para `--top abc`, half-up com 2 mutações, amostra só falha por mutação) aceitos.
- Apontamentos de baixa severidade: formatação Markdown da seção 8 corrigida pelo orquestrador; `_run` fixa `PYTHONPATH` em `src/` (aceito, não bloqueia).
