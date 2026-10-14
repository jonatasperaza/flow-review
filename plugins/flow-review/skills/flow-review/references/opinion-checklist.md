# Checklist de opinião

Percorra os itens contra o fluxo mapeado. Só vira achado o que você consegue apontar no código. O objetivo é lógica do fluxo, não estilo.

## Correção
- A falha é detectada pelo mecanismo certo? (código de saída/exceção vs. procurar texto na saída). Texto gera falso positivo e falso negativo.
- Todo caminho de erro termina em estado coerente? Para cada passo: se morrer aqui, o que fica gravado?
- Há `except` que engole erro (`pass`) ou função que devolve string de erro em vez de levantar exceção?
- Estado final reflete a realidade (ex.: "RUNNING" depois de cancelar algo que ainda roda)?

## Concorrência
- Dois gatilhos ao mesmo tempo (webhook + clique manual, dois pushes seguidos) geram o quê?
- A guarda de estado é atômica (update condicional) ou é ler-e-depois-gravar?
- Retentativas são idempotentes? Dedupe cobre reenvio ou também eventos distintos?

## Tempo e recursos
- Cada chamada externa tem timeout (conexão e execução)? Streaming costuma esquecer.
- O limite da fila (hard/soft) permite limpeza? O que acontece com o estado quando o worker é morto?
- Há algo que acumula (logs, volumes, caches) sem limpeza?

## Fronteiras e segurança do fluxo
- O gatilho público é autenticado? E se o segredo estiver ausente: falha fechado ou aberto?
- Credenciais atravessam o fluxo: onde são montadas, onde são logadas, onde são mascaradas?
- A identidade do destino é verificada (host key, certificado)?

## Observabilidade
- Quem descobre que o fluxo falhou, e quão rápido? Existe log, status externo, alerta?
- Dá para reconstruir o que aconteceu a partir do que é gravado?

## Simplificação
- Passos duplicados, validações repetidas em dois lugares, abstrações que só têm uma implementação.
- Acoplamento que obriga mudar vários arquivos para alterar uma regra.

## Preservar
- O que o fluxo já faz bem e não pode se perder numa refatoração (dedupe, mascaramento, auditoria, testes). Registre como "manter".

## Severidade
- **alta**: perde dado, expõe segredo/acesso, deixa o sistema em estado errado de forma comum.
- **média**: falha em condições plausíveis, mas recuperável; ou risco real que depende de configuração.
- **baixa**: dívida técnica, clareza, robustez marginal.
Se a severidade depende de configuração, escreva qual.
