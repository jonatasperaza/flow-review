# Onde procurar o fluxo, por stack

Siga sempre do gatilho ao efeito final. Procure pelas fronteiras: onde o fluxo entra, onde sai do processo (fila, rede, hardware) e onde grava estado.

## Django / DRF / Celery
- Entradas: `urls.py` (inclui webhooks), `views.py` / `viewsets` (`@action`), signals, comandos de `management/`, tasks agendadas (celery beat).
- Fila: `tasks.py` (`@shared_task`, `.delay`, `.apply_async`), `CELERY_*` em settings (time limits, retries, acks_late).
- Lógica: use cases, services, mixins. Em arquitetura hexagonal: `ports/` (contratos), `adapters/` (implementações), `use_cases/`.
- Estado: campos `status` nos models e quem os altera. Procure por transições sem guarda (check-then-set sem atomicidade).
- Erros: `except` genéricos, retornos de string no lugar de exceções, `pass` silencioso.

## Vue 3 / Pinia / Vuetify
- Rotas (`router`), guards, stores Pinia (actions que chamam API), composables, interceptors de HTTP.
- Fluxo = rota → componente → store/action → endpoint → atualização de estado → UI.

## FastAPI / Flask
- Rotas, dependências (`Depends`), middlewares, background tasks, clientes de serviços externos.

## ESP32 / firmware (Arduino, PlatformIO)
- `setup()` e `loop()`, handlers de interrupção, callbacks MQTT/HTTP, máquinas de estado, timeouts e watchdog.
- Fluxo físico: sensor → leitura → decisão → atuador → telemetria. Anote o que acontece offline.

## ThingsBoard
- Rule chains (JSON exportado): nós, conexões (Success/Failure), scripts de transformação. Fluxo = ponto de entrada (device telemetry) → nós → saída (alarme, RPC, API).
- Dependências de dados que o código não mostra (atributos do device, regras salvas só na UI) são `inferido`.

## Dokku / Docker / CI
- `Procfile`, `app.json`, `Dockerfile`, `.github/workflows/*.yml` (gatilhos: `push`, `pull_request`), crons de manutenção.
- Comportamento do Dokku (locks, zero downtime, rollback) é conhecimento externo: marque `inferido` a menos que haja doc no repo.

## Eventos assíncronos (MQTT, webhooks, filas)
Análise estática não enxerga quem publica. Registre o produtor como nó externo e marque `inferido` o que ele envia. Se a pessoa souber o contrato, pergunte.
