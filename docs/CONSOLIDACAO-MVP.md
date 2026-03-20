# Consolidação do MVP do C2-TA

## Arquivos de consolidação adicionados

- `triagem/mvp_urls.py`
- `triagem/admin_mvp.py`

## Objetivo

Esses arquivos juntam em um só ponto:

- rotas operacionais do MVP
- tela inicial baseada no painel
- registros de admin para modelos de integração e cidadão

## Como consolidar no núcleo atual

### URLs

No arquivo principal de URLs do app, substituir o include atual por:

```python
path('', include('triagem.mvp_urls'))
```

### Admin

Além do admin atual, importar o módulo:

```python
import triagem.admin_mvp
```

ou mover o conteúdo de `admin_mvp.py` para `admin.py`.

## Resultado esperado

Depois da consolidação, o projeto passa a ter:

- `/painel/`
- `/operacional/cidadaos/novo/`
- `/operacional/senhas/emitir/`
- painel como rota inicial do MVP
- admin com espelhos do ERP, fila de sincronização e extensão do cidadão

## Próximos passos

1. gerar migrations
2. criar bootstrap de unidades e serviços
3. criar chamada de senha
4. criar sincronização real com ERP
5. subir no Portainer para visualização
