# CLAUDE.md — Teste técnico Onfly (consolidador de reservas)

Objetivo: corrigir os defeitos da CLI `onfly_report` para que `pytest -q` passe e o relatório siga o `README.md` (fonte da verdade).
Mapa do repositório: `llm.txt`. Contrato do relatório: `docs/SCHEMA.md` (**obrigatório preservar**).

## Restrições invioláveis
- NÃO alterar os testes fornecidos: `tests/helpers.py`, `tests/test_currency.py`, `tests/test_nights.py`,
  `tests/test_regression_report.py`, `tests/test_status_rules.py`, `tests/test_top_hotels.py`. Só adicionar novos `test_*.py`.
- NÃO alterar `data/reservas_hoteis.csv` nem `data/taxas_cambio.csv`.
- NÃO alterar comando/argumentos da CLI nem schema/semântica do JSON (`docs/SCHEMA.md`).
- Os dados estão corretos; defeitos estão em `src/`.
- Python 3.11, só biblioteca padrão em runtime.

## Comandos
```bash
source .venv/bin/activate
pytest -q
ruff check src tests
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

## Regras de negócio (resumo — detalhes no README.md)
- Pipeline: ler → converter tipos → contar status → filtrar CONFIRMED → agregar.
- Só `CONFIRMED` entra em noites, valores, `by_month`, `top_hotels`. CANCELLED/NO_SHOW só nas contagens.
- `room_nights = (checkout - checkin).days * rooms` (não inclusivo; datas civis `YYYY-MM-DD`).
- BRL = `amount * rate_to_brl`. Dinheiro sempre `Decimal`; arredondar só na serialização, 2 casas, `ROUND_HALF_UP`.
- `average_nightly_rate_brl = total / noites`; sem noites → `"0.00"`.
- `by_month` pelo mês do check-in, asc. `top_hotels`: `total_brl` desc, empate `hotel_id` asc, limitado por `--top` (≥1).
- Exit codes: 0 sucesso, 2 entrada/argumento inválido, 1 erro inesperado.

---

## Fluxo agêntico (SDD + TDD)

### Papéis
| Papel | Quem | Pode editar | Responsabilidade |
|-|-|-|-|
| Orquestrador | Sessão principal | `specs/`, `entrega/`, docs | Planeja, escreve/aprova specs, dispara subagents, consolida resultados, decide. **Não implementa código** salvo escalonamento. |
| `investigador` | subagent | nada | Encontra defeitos e evidências num escopo; alimenta a spec. |
| `implementador` | subagent | `src/`, novos `tests/test_*.py` | Executa UMA spec aprovada em TDD (RED → GREEN → REFACTOR). |
| `revisor` | subagent | nada | Verifica a entrega da spec contra o DoD, restrições e schema. |

### Ciclo por tarefa
1. **Investigar** — orquestrador dispara `investigador` (um escopo por agente; podem rodar em paralelo).
2. **Especificar** — orquestrador cria `specs/NNN-<slug>.md` a partir de `specs/TEMPLATE.md`, registra em `specs/README.md` e abre uma issue no GitHub (label `spec`) com o conteúdo da spec, vinculando o link na spec e no registro (status `draft` → `approved`).
3. **Implementar** — dispara `implementador` com o caminho da spec. Ele:
   a. escreve os testes novos propostos e prova o **RED** (registra a saída na spec);
   b. faz a mudança mínima até **GREEN** (testes novos + imutáveis esperados);
   c. roda a suíte inteira + `ruff`; registra evidências na spec.
4. **Revisar** — dispara `revisor` com a spec. Reprovação volta ao passo 3 com os apontamentos.
5. **Fechar** — orquestrador marca `done` no registro, atualiza `entrega/README-ENTREGA.md`, faz commit (um por spec) em branch `spec/NNN-<slug>`, abre PR com `Closes #<issue>`.

### Escalonamento
Subagents devolvem `STATUS: ESCALATE` com motivo quando: a spec é ambígua/contradiz o README; a correção exige
tocar arquivo proibido ou mudar schema; o RED não reproduz; 2 tentativas de GREEN falharam; o achado está fora do escopo.
Só nesses casos o orquestrador intervém diretamente (ajusta spec, redivide tarefa ou implementa).

### Regras gerais
- Uma spec = um defeito (ou conjunto indivisível) = um commit.
- Achados de subagent são hipóteses até haver teste RED.
- Specs nunca são apagadas; specs abandonadas ficam `cancelled` com motivo.
- Exportação de sessões (ao final, em `entrega/uso-de-ia/`): `/export` da sessão principal → `sessao-NN.md`
  **e** export do app (menu da sessão › Export, zip com subagents) descompactado em `sessao-NN-completa/`.
  `entrega/uso-de-ia/declaracao.md` registra o que a IA fez vs. o candidato.

## CI
`.github/workflows/ci.yml` roda em push/PR: guarda de arquivos imutáveis, ruff, teste de contrato de schema
(`tests/test_schema_contract.py`), suíte completa e smoke da CLI na amostra. PR que altera `src/` deve incluir/atualizar uma spec.
