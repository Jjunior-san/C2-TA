# Roteiro operacional do C2-TA no Portainer

## Etapa 1 — consolidar o núcleo do projeto

Aplicar a troca final descrita em:

- `docs/TROCA-FINAL-DO-NUCLEO.md`

Arquivos-base da troca:

- `config/urls_portainer_ready.py`
- `triagem/admin_consolidated.py`
- `triagem/models_registry.py`

## Etapa 2 — gerar migrations

Depois da troca final, executar dentro do projeto:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Etapa 3 — publicar no GitHub

Subir para o repositório a consolidação final já aplicada.

## Etapa 4 — criar stack no Portainer

Usar:

- `stack.portainer.yml`

Como referência de variáveis:

- `env.portainer.sample`

## Etapa 5 — preencher variáveis críticas

Definir pelo menos:

- `POSTGRES_PASSWORD`
- `DJANGO_SECRET_KEY`
- `C2TA_ADMIN_PASSWORD`
- `C2TA_ERP_BASE_URL`
- `C2TA_ERP_API_TOKEN`
- `C2TA_WEBHOOK_SECRET`

## Etapa 6 — subir a stack

Após deploy bem-sucedido, entrar no container `web` e executar:

```bash
python manage.py bootstrap_c2ta
python manage.py check_external_base
```

## Etapa 7 — validar no navegador

Validar:

- `/admin/`
- `/painel/`
- `/operacional/cidadaos/novo/`
- `/operacional/senhas/emitir/`
- `/guiche/chamar-proximo/`

## Etapa 8 — teste funcional mínimo

1. Cadastrar um cidadão
2. Emitir uma senha
3. Ver senha no painel
4. Chamar a próxima senha
5. Confirmar chamada no painel
6. Validar comunicação com ERP

## Resultado esperado

Ao final dessa rotina, o C2-TA deve estar:

- publicado em stack separada
- com banco próprio
- com identidade C²
- com MVP operacional visível
- pronto para evolução do fluxo de atendimento
