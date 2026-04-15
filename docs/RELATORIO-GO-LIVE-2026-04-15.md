# Relatorio de Go-Live - C2-TA

Data: 2026-04-15
Escopo: validacao tecnica para subida controlada em homologacao/producao.

## 1. Mudancas aplicadas nesta rodada

- Hardening de concorrencia na emissao de senha:
  - `triagem/services.py`
  - uso de transacao atomica
  - lock de unidade com `select_for_update`
  - sequencia diaria baseada em `max(daily_sequence)` por unidade/dia
- Hardening de concorrencia na chamada de senha:
  - `triagem/call_service.py`
  - uso de transacao atomica
  - selecao da proxima senha com lock de linha
- Integridade de fila no modelo:
  - `triagem/models.py`
  - novo campo `issued_on`
  - constraints de unicidade por unidade/dia:
    - `daily_sequence`
    - `ticket_number`
- Hardening de configuracao Django:
  - `config/settings.py`
  - leitura de flags de seguranca por variaveis de ambiente
  - bloqueio de `SECRET_KEY` insegura com `DEBUG=0`
- Startup de container mais estrito:
  - `infra/docker/entrypoint.sh`
  - `migrate` e `collectstatic` nao silenciam falhas
- Variaveis adicionais documentadas:
  - `.env.example`

## 2. Testes adicionados

- `triagem/tests/test_services.py`
  - emissao de senha com sequencia diaria
  - erro para unidade inexistente
  - chamada da proxima senha e transicao de status
  - erro quando nao ha senha aguardando
- `triagem/tests/test_smoke.py`
  - smoke de rotas principais:
    - `/`
    - `/painel/`
    - `/operacional/cidadaos/novo/`
    - `/operacional/senhas/emitir/`
    - `/guiche/chamar-proximo/`

## 3. Checklist de pre-go-live

- Definir variaveis obrigatorias sem defaults inseguros:
  - `DJANGO_SECRET_KEY`
  - `C2TA_ADMIN_PASSWORD`
  - `C2TA_WEBHOOK_SECRET`
  - `C2TA_ERP_API_TOKEN`
- Garantir modo seguro em producao:
  - `DJANGO_DEBUG=0`
  - `DJANGO_SECURE_SSL_REDIRECT=1`
  - `DJANGO_SESSION_COOKIE_SECURE=1`
  - `DJANGO_CSRF_COOKIE_SECURE=1`
  - HSTS conforme politica de dominio
- Executar validacoes:
  - `python manage.py check`
  - `python manage.py test`
  - `python manage.py migrate`
  - `python manage.py bootstrap_c2ta`
  - `python manage.py check_external_base`
- Validar fluxo funcional minimo:
  - cadastro de cidadao
  - emissao de senha
  - chamada da proxima senha
  - painel de chamadas

## 4. Plano de rollback

### Rollback de aplicacao

1. Reverter para a imagem/tag anterior no Portainer.
2. Redeploy da stack.
3. Verificar healthchecks de `web` e `proxy`.

### Rollback de banco

1. Restaurar backup do banco anterior ao deploy.
2. Confirmar conectividade e acesso admin.
3. Executar smoke funcional minimo.

### Criticos para decidir rollback imediato

- erro em emissao/chamada de senha em fluxo basico
- indisponibilidade persistente de `web` apos redeploy
- falha de integridade de fila em ambiente real

## 5. Risco residual

- A base historica sem migrations versionadas ainda exige disciplina de deploy.
- Recomenda-se consolidar politica de migrations versionadas antes de escala operacional.
