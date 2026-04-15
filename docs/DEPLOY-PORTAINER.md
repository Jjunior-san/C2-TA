# Deploy do C2-TA no Portainer

## Arquivos principais

- `stack.portainer.yml`
- `env.portainer.sample`
- `Dockerfile`
- `infra/docker/entrypoint.sh`
- `infra/nginx/default.conf`

## Estratégia

O C2-TA sobe em stack separada do ERP, com:

- PostgreSQL próprio
- aplicação Django própria
- proxy Nginx próprio
- integração com o ERP por API

## Passos

1. Criar stack no Portainer usando `stack.portainer.yml`
2. Preencher as variáveis com base em `env.portainer.sample`
3. Definir domínio público do C2-TA
4. Definir token de integração com o ERP
5. Fazer deploy

## Quando usar este arquivo

Use `stack.portainer.yml` quando o Portainer estiver fazendo build local da aplicação e do proxy.

Se o deploy for em **Git repository**, prefira `stack.portainer.git.yml`.

Motivo: em modo Git, bind mounts de arquivos do repositório podem falhar no `proxy` dependendo de onde o engine resolve o caminho do checkout.

## Variáveis críticas

- `POSTGRES_PASSWORD`
- `DJANGO_SECRET_KEY`
- `C2TA_ADMIN_PASSWORD`
- `C2TA_ERP_BASE_URL`
- `C2TA_ERP_API_TOKEN`
- `C2TA_WEBHOOK_SECRET`

## Observação atual

A base de deploy já está preparada, mas o projeto ainda precisa consolidar os modelos no núcleo do app e gerar as migrations para um deploy plenamente funcional.
