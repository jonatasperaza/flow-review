# flow-review

Skill para Claude Code que transforma o fluxo de um sistema (hoje espalhado no código e na cabeça de quem escreveu) em documento versionado, com opinião crítica e decisões registradas.

## O que faz

1. Escolhe **um** fluxo delimitado.
2. Lê o código e mapeia do gatilho ao efeito final, com `arquivo:linha`.
3. Gera `flow.md` (diagrama Mermaid + tabela de passos, `verificado` vs `inferido`).
4. Opina em `decisions.md` (achados A-01…, severidade, evidência, custo).
5. Valida referências com `scripts/check_refs.py`.
6. Você aprova, reprova ou ajusta cada item. Só o aprovado é implementado.

## Instalação

```
/plugin marketplace add jonatasperaza/flow-review
/plugin install flow-review@flow-review
```

Ou use o arquivo `flow-review.skill` diretamente.

## Estrutura

```
.claude-plugin/marketplace.json
plugins/flow-review/
  .claude-plugin/plugin.json
  skills/flow-review/
    SKILL.md
    references/   extractors.md, opinion-checklist.md
    scripts/      check_refs.py
    templates/    flow.md, decisions.md
flow-review.skill   # pacote distribuível
```

## Uso

Peça: "analisa o fluxo de X", "quero mudar o fluxo de Y".

## Licença

MIT. Veja [LICENSE](LICENSE).
