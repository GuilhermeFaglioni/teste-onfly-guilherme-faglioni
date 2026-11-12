# Declaração de uso de IA

- **Ferramenta:** Claude Code (app desktop, aba Code)
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`)

## Fase 1 — Definição do fluxo de trabalho, documentação, testes de contrato e CI

### O que a IA fez
- Leu o `README.md` e resumiu o problema, as regras de negócio, o contrato da CLI e os requisitos de entrega.
- **Fluxo de trabalho:** redigiu o `CLAUDE.md`, que define:
  - a sessão principal como orquestradora;
  - os papéis dos agentes;
  - o ciclo SDD + TDD: investigar → spec → RED → GREEN → revisão → commit;
  - as regras de escalonamento.
- **Subagents:** criou `.claude/agents/investigador.md`, `implementador.md` e `revisor.md`, com as permissões de cada um (os de leitura não editam; o implementador só edita `src/` e testes novos).
- **Specs:** criou `specs/TEMPLATE.md`, com escopo, plano, testes imutáveis esperados, testes novos (RED antes do código), Definition of Done e evidências, e `specs/README.md`, o registro das specs.
- **Documentação:**
  - `docs/SCHEMA.md`: contrato do JSON e da CLI, de preservação obrigatória;
  - `llm.txt`: mapa de pastas e arquivos;
  - esqueletos de `entrega/README-ENTREGA.md` e desta declaração.
- **Testes:** escreveu `tests/test_schema_contract.py` (5 testes adicionais), que cobre:
  - as chaves exatas;
  - os tipos;
  - o formato do dinheiro;
  - a ordem de `by_month`;
  - o limite de `--top`;
  - a média sem noites.
- **CI:** criou `.github/workflows/ci.yml`, que faz:
  - bloqueio de alteração em testes fornecidos e em dados imutáveis;
  - exigência de spec quando `src/` muda;
  - ruff, teste de schema, pytest completo e execução da CLI na amostra e no dataset.
- Fez os commits: o projeto original como base e o fluxo agêntico em seguida.

### O que eu fiz
- Defini a estratégia:
  - sessão principal como orquestradora que só intervém quando há escalonamento;
  - subagents investigador, implementador e revisor;
  - SDD + TDD com RED → GREEN e Definition of Done;
  - registro de todas as specs.
- Defini os requisitos:
  - CI rodando os testes do PR;
  - testes de preservação do schema;
  - schema documentado para os agentes;
  - um `llm.txt`.
- Revisei e aprovei cada etapa: a leitura do problema, a criação dos artefatos, os commits e o push.

## Fase 2 — Investigação e especificação (SDD)

### O que a IA fez
- **Linha de base:** rodou o `pytest -q` antes de qualquer correção: 5 falhas (os testes fornecidos) e 5 testes passando (contrato de schema).
- **Investigação em paralelo:** atuando como orquestradora, disparou 3 subagents investigadores somente leitura, um para cada parte do código:
  - leitura dos CSVs e conversão de tipos;
  - regras de cálculo;
  - montagem do relatório e CLI.
- **Por que agentes genéricos:** os subagents de `.claude/agents/` só são carregados numa sessão nova. Por isso foram usados agentes `general-purpose` com a instrução de seguir `investigador.md`.
- **Consolidação:** reuniu os relatórios e conferiu as evidências. Confirmou no código o corte de 200 linhas e corrigiu uma conclusão de um investigador (o corte não afeta `test_regression_report`, que usa um CSV de 3 linhas).
- **Escalonamentos:** registrou os escalonamentos de escopo e as suspeitas descartadas (moeda sem taxa, status desconhecido).
- **Defeitos confirmados:** 5.
  - `status_policy`: NO_SHOW era faturado;
  - `stay_calculator`: subtraía o dia do mês em vez das datas;
  - `currency_converter`: dividia pela taxa e passava por float;
  - `report_builder`: ordenação de `top_hotels` invertida;
  - `csv_reservation_repository`: leitura limitada a 200 linhas.
- **Lacunas de cobertura:** levantou o que os testes fornecidos não cobrem: exit codes, `--top`, half-up, mês do check-in e amostra de validação.
- **Specs:** redigiu as specs `specs/001` a `specs/006`, cada uma com escopo, causa raiz, plano, testes imutáveis esperados, testes novos com a falha esperada (RED) e Definition of Done.
- **RED por mutação:** propôs esse método para a spec 006, porque ela cobre comportamento que já está correto.
- **Issues:** criou o label `spec` e as issues #1 a #6 no GitHub. Vinculou cada issue à sua spec e ao registro `specs/README.md`.
- **Fluxo no `CLAUDE.md`:** atualizou com issue por spec, branch `spec/NNN-<slug>` e PR com `Closes #N`.

### O que eu fiz
- Autorizei a investigação.
- Defini que cada spec vira uma issue para acompanhamento.
- Revisei e aprovei as 6 specs (status `approved`).
- Autorizei o commit e o push.

## Fase 3 — Implementação (TDD)

### Validação da exportação de sessões
**O que a IA fez:**
- Exportou a sessão pelo app (zip em `~/Downloads`) e inspecionou o conteúdo: a transcrição principal e a de cada subagent, em JSONL, com prompt, comandos, resultados e relatório final.
- Comparou com o `/export` da CLI que eu testei, que mostra só a resposta final de cada subagent.
- Encontrou o e-mail do candidato em 2 trechos da transcrição principal. Ele vem do contexto injetado pelo app e precisa ser removido antes de publicar.
- Registrou a exportação dupla no `CLAUDE.md` e nesta declaração.

**O que eu fiz:**
- Testei o `/export` na Claude CLI com dois subagents.
- Decidi usar as duas exportações.

### SPEC-001 — Só CONFIRMED é faturável (issue #1, PR #7)
**O que a IA fez:**
- **Antes de começar:** como orquestradora, conferiu que a worktree estava limpa, enviou o commit pendente e criou o branch `spec/001-status-faturavel`.
- **Implementação:** disparou um subagent implementador (`general-purpose` seguindo `implementador.md`):
  - escreveu `tests/test_status_policy_extra.py` com 5 testes;
  - comprovou o RED, com 3 falhas: NO_SHOW, status desconhecido e a CLI com 4 noites em vez de 1;
  - aplicou a correção em `status_policy.py` (`status == "CONFIRMED"`);
  - comprovou o GREEN: 11 testes passando e 4 falhando, essas das specs 002 a 004; ruff limpo; schema 5/5;
  - registrou as evidências na spec.
- **Revisão:** disparou um subagent revisor (`general-purpose` seguindo `revisor.md`):
  - conferiu o escopo do diff e que nenhum arquivo proibido mudou;
  - conferiu o RED antes do GREEN e o DoD;
  - na amostra de validação, as contagens batem com o README (12/9/2/1);
  - veredito: APROVADO, com 2 apontamentos de baixa severidade.
- **Fechamento:**
  - conferiu o diff e o pytest de forma independente;
  - resolveu os apontamentos e marcou a spec como `done`;
  - atualizou `specs/README.md` e `entrega/README-ENTREGA.md`;
  - fez o commit e o push e abriu o PR #7.
- **Merge:**
  - analisou a CI: guarda, ruff, schema e testes da spec passaram;
  - a "Suíte completa" falhou só nos 4 testes das specs abertas (falha esperada);
  - fez o merge com `--delete-branch` e confirmou que a issue #1 foi fechada.

**O que eu fiz:**
- Autorizei o início da implementação.
- Defini a condição para o merge: só se passasse nos testes e critérios de aceite da spec.
- Decidi fazer o merge da 001 antes de iniciar a 002.

### SPEC-002 a 006
_A preencher._

## Sessões exportadas
_Pendente._ Nenhuma sessão foi exportada até agora. Ao final do trabalho serão feitas duas exportações complementares, em `entrega/uso-de-ia/`:
- `sessao-01.md` — `/export` do Claude Code: sessão principal (orquestradora) em texto legível. Não inclui subagents.
- `sessao-01-completa/` — export do app (menu da sessão › Export), descompactado: transcrição principal e de cada subagent em JSONL nativo (`subagents/agent-<id>.jsonl` + `.meta.json` com tipo e tarefa).

Subagents previstos: 3 investigadores (Fase 2) e os implementadores/revisores da Fase 3.
