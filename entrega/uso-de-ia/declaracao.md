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
- Encontrou o e-mail do candidato em 2 trechos da transcrição principal. Ele vem do contexto injetado pelo app. Por decisão do candidato, o e-mail é mantido no export.
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
- Acompanhei o processo de implementação feito pelos subagents.
- Fiz o code review do PR #7 antes de permitir o merge.
- Defini a condição para o merge: só se passasse nos testes e critérios de aceite da spec.
- Decidi fazer o merge da 001 antes de iniciar a 002.

### Export parcial da sessão
**O que a IA fez:**
- Exportou a sessão e a descompactou em `sessao-01-completa/`.
- Num primeiro momento removeu o e-mail. Depois reverteu e manteve o export original.
- Fez o commit e o push.

**O que eu fiz:**
- Pedi o export.
- Decidi manter o e-mail no export.
- Autorizei o commit.

### SPEC-002 — Noites pela diferença de datas (issue #2, PR #8)
**O que a IA fez:**
- **Antes de começar:** criou o branch `spec/002-noites-nao-inclusivas` a partir de `main`, já com a 001.
- **Implementação:** disparou um subagent implementador (`general-purpose` seguindo `implementador.md`):
  - escreveu `tests/test_stay_calculator_extra.py` com 5 testes;
  - comprovou o RED, com 4 falhas: -28, -29, -56 e -27;
  - aplicou a correção em `stay_calculator.py` (`(checkout - checkin).days * rooms`);
  - comprovou o GREEN: 17 testes passando e 3 falhando, essas das specs 003 e 004; ruff limpo.
- **Revisão:** disparou um subagent revisor (`general-purpose` seguindo `revisor.md`):
  - conferiu o escopo do diff;
  - na amostra de validação, `total_room_nights` 28 e `by_month` 25/3 batem com o README;
  - veredito: APROVADO.
- **Fechamento:**
  - conferiu o diff e o pytest de forma independente;
  - marcou a spec como `done`;
  - atualizou `specs/README.md` e `entrega/README-ENTREGA.md`;
  - fez o commit e o push e abriu o PR #8.
- **Auto-fix:**
  - analisou o evento de falha da CI: só a "Suíte completa", nos 3 testes das specs abertas;
  - não alterou nada, para não misturar specs no PR;
  - após autorização, fez o merge e confirmou que a issue #2 foi fechada.
- **Subagents nativos:** registrou que, depois do merge, os subagents de `.claude/agents/` passaram a ficar disponíveis como tipos nativos nesta sessão.

**O que eu fiz:**
- Autorizei o início da spec.
- Acompanhei o processo de implementação feito pelos subagents.
- Fiz o code review do PR #8 antes de permitir o merge.
- Autorizei o merge com o mesmo critério da 001.

### Atualização da declaração e do export (antes da SPEC-003)
**O que a IA fez:**
- Registrou a SPEC-002 e os code reviews do candidato nesta declaração.
- Refez o export da sessão (principal mais 7 subagents) e fez o commit e o push.

**O que eu fiz:**
- Pedi o export e a atualização da declaração.
- Informei que fiz o code review dos PRs #7 e #8.

### SPEC-003 — Câmbio por multiplicação em Decimal (issue #3, PR #9)
**O que a IA fez:**
- **Antes de começar:** criou o branch `spec/003-cambio-multiplicacao-decimal` a partir de `main`.
- **Implementação:** pela primeira vez usou os subagents **nativos** `implementador` e `revisor`, com as permissões de ferramentas definidas em `.claude/agents/`. O implementador:
  - escreveu `tests/test_currency_extra.py` com 3 testes;
  - comprovou o RED, com 2 falhas: multiplicação e Decimal exato;
  - aplicou a correção em `currency_converter.py` (`amount * rates[currency]`, sem float);
  - comprovou o GREEN: 22 testes passando e 1 falhando, essa da spec 004; ruff limpo.
- **Divergência da previsão:** o implementador relatou que `test_regression_report` passou antes do previsto pela spec.
- **Revisão:** o revisor:
  - confirmou que não sobrou `float` em `src/`;
  - na amostra de validação, `total_amount_brl` 7566.00, `average_nightly_rate_brl` 270.21 e `by_month` batem com o README;
  - explicou a divergência: o teste só verifica `summary`, e o câmbio era o último defeito que o afetava;
  - veredito: APROVADO.
- **Fechamento:**
  - conferiu o diff e o pytest de forma independente;
  - corrigiu a previsão errada na seção 5 da spec;
  - marcou a spec como `done`;
  - atualizou `specs/README.md` e `entrega/README-ENTREGA.md`;
  - fez o commit e o push e abriu o PR #9.
- **Merge:**
  - conferiu a CI: só `test_top_hotels` falhou (esperado);
  - fez o merge e confirmou que a issue #3 foi fechada;
  - recebeu depois um evento atrasado do Auto-fix sobre o PR já mesclado e não fez nada.

**O que eu fiz:**
- Autorizei o início da spec.
- Acompanhei o processo de implementação feito pelos subagents.
- Fiz o code review do PR #9 antes de permitir o merge.
- Autorizei o merge.

### Atualização da declaração e do export (antes da SPEC-004)
**O que a IA fez:**
- Registrou a SPEC-003.
- Refez o export da sessão (principal mais 9 subagents) e fez o commit e o push.

**O que eu fiz:**
- Pedi o export e a atualização da declaração antes de iniciar a spec.

### SPEC-004 — top_hotels por total desc e hotel_id asc (issue #4, PR #10)
**O que a IA fez:**
- **Antes de começar:** criou o branch `spec/004-ordenacao-top-hotels` e, antes de disparar o implementador, corrigiu duas coisas na spec:
  - a previsão de `test_regression_report`, que já passava desde a 003;
  - a referência de linha do defeito (`report_builder.py:91`).
- **Implementação:** o subagent nativo `implementador`:
  - escreveu `tests/test_top_hotels_extra.py`;
  - comprovou o RED: 2 testes novos e o `test_top_hotels` fornecido falhando;
  - aplicou a correção com a chave `(-total, hotel_id)`;
  - comprovou o GREEN: **26 testes passando (100%)**;
  - na amostra, `top_hotels` bate com o README.
- **Desvio registrado pelo implementador:** o teste de empate ganhou um terceiro hotel, porque só com H01 e H02 empatados não haveria RED.
- **Revisão:** o subagent nativo `revisor`:
  - validou o desvio: o teste também pegaria uma correção ingênua com `reverse=True`;
  - na amostra, o relatório bate integralmente com o README (summary, `by_month` e `top_hotels`);
  - no dataset completo, a CLI sai com código 0 (`total_reservations` 200 até a SPEC-005);
  - veredito: APROVADO, com 3 apontamentos de baixa severidade.
- **Fechamento:**
  - atualizou a tabela da seção 6 da spec;
  - marcou a spec como `done`;
  - atualizou `specs/README.md` e `entrega/README-ENTREGA.md`;
  - abriu o PR #10.
  - O apontamento 2 (`test_fewer_hotels_than_top` não verificava a ordem) ficou inicialmente sem aplicar, com justificativa.
- **Ajuste pós-revisão:** a pedido do candidato, devolveu o apontamento ao **mesmo** implementador (retomado com contexto) no mesmo branch. Ele:
  - alterou o teste para verificar a ordem;
  - provou o RED recolocando temporariamente a chave antiga, reverteu e confirmou `src/` idêntico ao HEAD.
  - A IA conferiu, anotou a seção 8 da spec para manter a coerência e enviou o commit ao PR #10.
- **Merge:** a CI ficou **toda verde** pela primeira vez. A IA fez o merge e confirmou que a issue #4 foi fechada.

**O que eu fiz:**
- Autorizei o início da spec.
- Acompanhei o processo de implementação feito pelos subagents.
- Questionei qual apontamento do revisor ficou sem aplicar e decidi devolvê-lo ao implementador.
- Fiz o code review do PR #10, inclusive do ajuste, antes de permitir o merge.
- Autorizei o merge.

### Atualização da declaração e do export (antes da SPEC-005)
**O que a IA fez:**
- Registrou a SPEC-004.
- Refez o export da sessão (principal mais 11 subagents) e fez o commit e o push.

**O que eu fiz:**
- Pedi o export e a atualização da declaração antes de iniciar a spec.

### SPEC-005 — Ler todas as reservas do CSV (issue #5, PR #11)
**O que a IA fez:**
- **Antes de começar:** criou o branch `spec/005-leitura-sem-limite-linhas` e conferiu que a linha do defeito citada na spec estava correta.
- **Implementação:** o subagent nativo `implementador`:
  - escreveu `tests/test_reservation_repository_extra.py` com 250 linhas sintéticas via CLI e uma leitura do dataset real;
  - comprovou o RED: `200 == 250` e `200 == 300`;
  - removeu o corte de 200 linhas;
  - comprovou o GREEN: 28 testes passando;
  - rodou a CLI no dataset completo.
- **Revisão:** o subagent nativo `revisor`:
  - confirmou que `data/` ficou intacto e que não há outro corte de leitura em `src/`;
  - **recalculou o dataset completo de forma independente** (csv mais Decimal, sem o código da CLI) e obteve valores idênticos aos da CLI:
    - 300 reservas: 235 confirmadas, 31 canceladas e 34 no-show;
    - 1347 noites;
    - total de 396170.00 e média de 294.11;
  - confirmou que a amostra do README continua batendo integralmente;
  - veredito: APROVADO.
- **Fechamento:**
  - ajustou a descrição de um teste na seção 6 da spec (observação do revisor);
  - marcou a spec como `done`;
  - atualizou `specs/README.md` e `entrega/README-ENTREGA.md`;
  - abriu o PR #11.
- **Merge:** com a CI toda verde, fez o merge e confirmou que a issue #5 foi fechada. Com isso, os 5 defeitos estão corrigidos.

**O que eu fiz:**
- Autorizei o início da spec.
- Acompanhei o processo de implementação feito pelos subagents.
- Fiz o code review do PR #11 antes de permitir o merge.
- Autorizei o merge.

### Atualização da declaração e do export (antes da SPEC-006)
**O que a IA fez:**
- Registrou a SPEC-005.
- Refez o export da sessão (principal mais 13 subagents) e fez o commit e o push.

**O que eu fiz:**
- Pedi o export e a atualização da declaração antes de iniciar a spec.

### SPEC-006 — Testes de contrato da CLI e exatidão (issue #6, PR #12)
**O que a IA fez:**
- **Antes de começar:** criou o branch `spec/006-testes-contrato-cli`.
- **Implementação:** o subagent nativo `implementador`:
  - escreveu `tests/test_cli_contract_extra.py` com 9 testes:
    - exit 0/2/1;
    - `--top` 0, -1 e abc;
    - half-up após a soma;
    - mês do check-in;
    - amostra completa do README.
  - Todos passaram sem mutação, ou seja, não havia defeito oculto.
  - Comprovou o **RED por mutação**: aplicou cada mutação no código, mostrou a falha e reverteu. No fim, `src/` ficou inalterado.
  - Declarou 3 desvios da tabela da spec.
- **Revisão:** o subagent nativo `revisor`:
  - reproduziu 5 mutações numa cópia do código **fora do repositório**;
  - conferiu os valores do teste da amostra com o README e verificou o determinismo;
  - aceitou os desvios;
  - veredito: APROVADO, com 2 apontamentos de baixa severidade.
- **Fechamento:**
  - corrigiu a formatação Markdown da seção 8 da spec (apontamento do revisor);
  - marcou a spec como `done`;
  - registrou os testes como "lacuna de cobertura" em `README-ENTREGA.md`;
  - abriu o PR #12.
- **Merge:** com a CI toda verde, fez o merge. Todas as issues (#1 a #6) ficaram fechadas.

**O que eu fiz:**
- Autorizei o início da spec.
- Acompanhei o processo de implementação feito pelos subagents.
- Fiz o code review do PR #12 antes de permitir o merge.
- Autorizei o merge.

## Fase 4 — Fechamento da entrega

**O que a IA fez:**
- Completou `entrega/README-ENTREGA.md`: como investigou, como validar, resultados da amostra e do dataset completo, e a saída final do `pytest` (37 passed) e do `ruff`.
- Conferiu que os testes fornecidos, `data/reservas_hoteis.csv`, `data/taxas_cambio.csv` e `README.md` estão idênticos ao commit original.
- Atualizou esta declaração e o export da sessão.

**O que eu fiz:**
- Autorizei a finalização.
- Revisei a documentação de entrega. _(pendente)_
- Confirmei que o export do app contém a sessão inteira (principal e subagents) e o defini como fonte única, já que o `/export` não funciona no Claude Desktop App.

## Resumo da divisão de trabalho
- **IA (Claude Code, Opus 5.5):**
  - escreveu toda a documentação de processo (`CLAUDE.md`, subagents, template e registro de specs, `docs/SCHEMA.md`, `llm.txt`, CI);
  - orquestrou 15 subagents (3 investigadores, mais 1 implementador e 1 revisor por spec) e 1 retomada de implementador para o ajuste pós-revisão;
  - escreveu as specs;
  - por meio dos subagents, escreveu os testes e as correções;
  - conferiu cada entrega e operou o git e o GitHub (issues, PRs, merges).
- **Eu:**
  - defini a estratégia: orquestração com subagents, SDD + TDD, issues por spec, CI com preservação do schema e exportação dupla;
  - aprovei as specs;
  - acompanhei cada implementação;
  - fiz o code review de todos os PRs (#7 a #12) antes de autorizar cada merge;
  - decidi pontos específicos, como devolver o apontamento da SPEC-004 ao implementador e manter o e-mail no export.

## Sessões exportadas
**Fonte única:** `sessao-01-completa/`, o export do Claude Desktop App (menu da sessão › Export, zip descompactado sem alterações).

Ele contém:
- `transcript.jsonl`: a conversa completa da sessão principal (orquestradora), com cada prompt, resposta, chamada de ferramenta e resultado.
- `<sessão>/subagents/agent-<id>.jsonl`: a conversa completa de cada um dos **15 subagents**, com prompt recebido, comandos, resultados e relatório final (`SubagentHandback`).
- `<sessão>/subagents/agent-<id>.meta.json`: tipo do agente (`general-purpose`, `implementador`, `revisor`), tarefa e status.
- `metadata.json` e `local-session-state.json`: metadados da sessão.

Subagents incluídos:
- 3 investigadores (Fase 2);
- 1 implementador e 1 revisor por spec, de 001 a 006 (Fase 3);
- a retomada do implementador da SPEC-004 está no mesmo arquivo dele.

**Por que não há `/export`:** o comando `/export` não funciona no Claude Desktop App, onde a sessão foi conduzida. Num teste à parte na Claude CLI, ele também mostrou apenas a resposta final de cada subagent, sem o trabalho interno. O export do app foi verificado e cobre a sessão inteira, então ficou como fonte única.

O formato é JSONL, que é o nativo da ferramenta e é aceito pelo README do teste.
