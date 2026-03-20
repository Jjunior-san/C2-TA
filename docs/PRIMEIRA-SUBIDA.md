# Primeira subida do C2-TA

## Passo 1

Criar a stack com `stack.portainer.yml`.

## Passo 2

Preencher as variáveis com base em `env.portainer.sample`.

## Passo 3

Garantir principalmente:

- `POSTGRES_PASSWORD`
- `DJANGO_SECRET_KEY`
- `C2TA_ADMIN_PASSWORD`
- `C2TA_ERP_BASE_URL`
- `C2TA_ERP_API_TOKEN`
- `C2TA_WEBHOOK_SECRET`

## Passo 4

Depois da stack subir, executar o bootstrap inicial:

```bash
python manage.py bootstrap_c2ta
```

## Passo 5

Testar comunicação externa:

```bash
python manage.py check_external_base
```

## Resultado esperado

- aplicação sobe
- admin responde
- unidade `CENTRAL` existe
- serviços iniciais existem
- comunicação com ERP pode ser testada

## Observação

Antes da primeira subida definitiva, ainda será necessário consolidar os modelos e gerar as migrations do projeto.
