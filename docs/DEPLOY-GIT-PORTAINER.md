# Deploy do C2-TA via Git no Portainer

## Arquivos usados

- `stack.portainer.git.yml`
- `.github/workflows/publish-ghcr.yml`
- `infra/nginx/Dockerfile`
- `Dockerfile`

## Estratégia

1. O GitHub Actions publica as imagens no GHCR.
2. O Portainer lê a stack direto do Git.
3. A stack usa `image:` em vez de `build:`.
4. O deploy não depende de build local no Portainer.

## Passo 1 — garantir publicação das imagens

No GitHub, deixar habilitado o workflow:

- `.github/workflows/publish-ghcr.yml`

A cada push no `main`, devem ser publicadas:

- `ghcr.io/jjunior-san/c2-ta-web:latest`
- `ghcr.io/jjunior-san/c2-ta-proxy:latest`

## Passo 2 — criar stack no Portainer

Em **Stacks > Add stack > Git repository**:

- Repository URL: `https://github.com/Jjunior-san/C2-TA.git`
- Reference: `main`
- Compose path: `stack.portainer.git.yml`

## Passo 3 — variáveis críticas

Definir no Portainer:

- `POSTGRES_PASSWORD`
- `DJANGO_SECRET_KEY`
- `C2TA_ADMIN_PASSWORD`
- `C2TA_ERP_BASE_URL`
- `C2TA_ERP_API_TOKEN`
- `C2TA_WEBHOOK_SECRET`

Opcionalmente:

- `C2TA_WEB_IMAGE`
- `C2TA_PROXY_IMAGE`

## Passo 4 — primeira execução pós-deploy

Entrar no container `web` e executar:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py bootstrap_c2ta
python manage.py check_external_base
```

## Resultado esperado

- stack publicada pelo Git no Portainer
- imagens vindas do GHCR
- banco separado
- MVP visível
- integração externa testável
