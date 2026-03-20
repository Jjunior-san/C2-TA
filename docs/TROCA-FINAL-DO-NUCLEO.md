# Troca final do núcleo do C2-TA

## Arquivos prontos para a rodada final

- `config/urls_portainer_ready.py`
- `triagem/admin_consolidated.py`
- `triagem/models_registry.py`

## Objetivo

Esses arquivos reúnem a base final do MVP para:

- roteamento raiz consolidado
- admin consolidado
- mapa central dos modelos do app

## Como aplicar

### 1. URLs do projeto

Trocar o conteúdo principal de `config/urls.py` pelo conteúdo de:

- `config/urls_portainer_ready.py`

### 2. Admin do app

Trocar o conteúdo principal de `triagem/admin.py` pelo conteúdo de:

- `triagem/admin_consolidated.py`

### 3. Núcleo de modelos

Usar `triagem/models_registry.py` como referência oficial da consolidação do app.

## Depois da troca

Executar:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py bootstrap_c2ta
python manage.py check_external_base
```

## Resultado esperado

- admin consolidado
- painel do MVP navegável
- operação de cidadão, senha e chamada pronta para teste
- base pronta para primeira publicação visual no Portainer
