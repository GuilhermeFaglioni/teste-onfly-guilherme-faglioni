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

## Fase 2 — Correção dos defeitos
_A preencher._

## Sessões exportadas
- `sessao-01.md` — sessão principal (definição do fluxo e correções).
