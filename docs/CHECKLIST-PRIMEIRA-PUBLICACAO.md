# Checklist da primeira publicação do C2-TA

## 1. Consolidação do núcleo

- [ ] Ligar `triagem/mvp_urls.py` ao roteamento principal
- [ ] Ligar `triagem/call_urls.py` ao roteamento do app
- [ ] Ligar `triagem/operations_urls.py` ao roteamento do app
- [ ] Importar `triagem/admin_mvp.py` no admin principal
- [ ] Consolidar `triagem/integration_models.py` no núcleo do app
- [ ] Consolidar `triagem/citizen_profile.py` no núcleo do app

## 2. Banco e migrations

- [ ] Gerar migrations
- [ ] Aplicar migrations no ambiente local
- [ ] Validar subida com banco limpo

## 3. Bootstrap funcional

- [ ] Rodar `python manage.py bootstrap_c2ta`
- [ ] Confirmar criação da unidade `CENTRAL`
- [ ] Confirmar criação dos serviços iniciais

## 4. Integração externa

- [ ] Preencher `C2TA_ERP_BASE_URL`
- [ ] Preencher `C2TA_ERP_API_TOKEN`
- [ ] Rodar `python manage.py check_external_base`
- [ ] Validar comunicação com ERP

## 5. Interface e operação

- [ ] Validar home/painel
- [ ] Validar cadastro de cidadão
- [ ] Validar emissão de senha
- [ ] Validar chamada da próxima senha
- [ ] Validar painel de chamadas

## 6. Portainer

- [ ] Criar stack com `stack.portainer.yml`
- [ ] Definir variáveis do arquivo `env.portainer.sample`
- [ ] Validar healthcheck do `web`
- [ ] Validar healthcheck do `proxy`

## 7. Domínio e acesso

- [ ] Publicar domínio do C2-TA
- [ ] Validar acesso HTTPS
- [ ] Validar `/admin`
- [ ] Validar `/painel/`
- [ ] Validar fluxo operacional do MVP
