---
name: flow-review
description: Mapeia o fluxo real de um sistema a partir do código (rotas, tasks, filas, eventos, integrações), desenha o diagrama com referências arquivo:linha, dá opinião crítica item a item e deixa o usuário aprovar, reprovar ou ajustar cada achado antes de qualquer mudança. Use sempre que o usuário pedir para "analisar o fluxo", "entender como X funciona hoje", "desenhar o fluxo do código", "revisar a lógica de um processo", "opinar sobre o fluxo", "quero mudar o fluxo de X" ou quiser aprovar/reprovar mudanças de fluxo, mesmo que não diga "skill" nem "diagrama". Não use para auditoria genérica de qualidade (expert-review) nem para implementar mudanças sem antes passar pela revisão do fluxo.
---

# flow-review

Transforma o fluxo que hoje vive na cabeça de quem escreveu o código em um documento versionado, com opinião crítica e decisões registradas. A pessoa decide; você só implementa o que ela aprovou.

## Por que existe

Fluxos de sistema se perdem em três lugares: no código (espalhado em views, tasks e adapters), na memória de quem escreveu e em conversas soltas. O valor desta skill é juntar os três: mapa fiel ao código, opinião com evidência e decisão registrada. Por isso duas regras valem mais que o resto: **nada de fluxo inventado** (todo passo aponta para código real) e **nada de implementar sem aprovação**.

## Ciclo

1. **Escopo.** Escolha UM fluxo delimitado (ex.: "redeploy de app", "leitura de RFID até abrir a catraca"). Se o pedido for "o sistema inteiro", proponha 3 a 5 fluxos candidatos e peça para escolher um. Diagrama de sistema inteiro fica ilegível e ninguém revisa.
2. **Mapear.** Leia o código seguindo o fluxo da entrada até o efeito final: gatilho, validações, filas, chamadas externas, estado gravado, caminhos de erro. Use `references/extractors.md` para saber onde procurar em cada stack. Anote `arquivo:linha` enquanto lê, não depois.
3. **Escrever `flow.md`** a partir de `templates/flow.md`: diagrama Mermaid + tabela de passos. Cada passo tem ID (F1, F2...), evidência e tipo: `verificado` (você leu o código) ou `inferido` (depende de config externa, evento, comportamento de terceiros). Inferido nunca se disfarça de verificado.
4. **Opinar.** Passe pelo `references/opinion-checklist.md` e escreva os achados em `decisions.md` a partir de `templates/decisions.md`. Cada achado: ID (A-01...), severidade, evidência com `arquivo:linha`, o que está acontecendo, o que mudar, custo estimado. Só entra achado que você consegue apontar no código; palpite vira pergunta, não achado.
5. **Conferir.** Rode `python3 -I scripts/check_refs.py <flow.md> <raiz-do-repo>`. Ele falha se alguma referência apontar para arquivo ou linha que não existe. Corrija antes de mostrar qualquer coisa. Depois releia cada achado contra o código uma vez: opinião errada custa a confiança da pessoa.
6. **Decidir.** Mostre diagrama e achados e peça decisão por item: aprovar, reprovar ou ajustar (com comentário). Com até 4 achados relevantes use AskUserQuestion; com mais, liste todos e pergunte pelos de maior severidade primeiro. Registre a resposta em `decisions.md`.
7. **Implementar só o aprovado.** Itens reprovados ficam registrados com o motivo (a próxima rodada não deve sugerir a mesma coisa). Se nenhum item foi aprovado, pare aqui.

## Fluxo desejado

Se a pessoa descrever ou editar como gostaria que o fluxo fosse, escreva isso como `flow-desejado.md` no mesmo formato e liste o que muda entre os dois (passos novos, removidos, reordenados). O plano de implementação sai dessa diferença, não de uma conversa solta.

## Onde salvar

No repositório analisado: `docs/flows/<nome-do-fluxo>/flow.md` e `decisions.md`. Fluxo versionado junto ao código permite diff e revisão em PR. Se a pessoa não quiser mexer no repo, salve fora e diga onde ficou.

## Honestidade sobre o que você sabe

- Marque `inferido` sempre que o comportamento depender de algo que você não leu: comportamento do Dokku/Docker/Celery, configuração de produção, branch protection, variáveis de ambiente reais.
- Se um achado só vale em certas configurações, diga qual. Exemplo: "só se `GITHUB_WEBHOOK_SECRET` estiver vazio em produção".
- Não afirme que algo está quebrado em produção; afirme o que o código faz.
- Se algo bom no fluxo merece ser preservado (dedupe, mascaramento de credenciais, auditoria), registre também. Revisão só de defeitos desanima e esconde o que não pode ser perdido numa refatoração.

## Tamanho e nível de detalhe

O diagrama principal cabe em uma tela: no máximo ~15 nós. Se passar disso, quebre em subfluxos (ex.: "resolução do plano git" vira diagrama próprio) e referencie pelo ID. Prefira três diagramas legíveis a um completo e ilegível.

## Entrega

Entregue `flow.md` e `decisions.md`, e no chat um resumo curto: o fluxo em 3 a 5 linhas, os achados em ordem de severidade e a pergunta de decisão. Não repita o conteúdo dos arquivos.
