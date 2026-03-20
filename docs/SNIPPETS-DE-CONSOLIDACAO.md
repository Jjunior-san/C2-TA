# Snippets de consolidação do C2-TA

## 1. URLs principais do projeto

Use este padrão no arquivo principal de URLs:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('triagem.mvp_urls')),
]
```

## 2. URLs internas do app

Dentro do app, incluir as rotas operacionais e de guichê:

```python
from django.urls import include, path

from . import operations_views

app_name = 'triagem'

urlpatterns = [
    path('', operations_views.panel, name='home-panel'),
    path('operacional/', include('triagem.operations_urls')),
    path('operacional/', include('triagem.call_urls')),
    path('painel/', operations_views.panel, name='panel'),
]
```

## 3. Consolidação do admin

No `admin.py` principal, manter o admin atual e importar o módulo complementar:

```python
import triagem.admin_mvp
```

## 4. Organização dos modelos

Na consolidação final, reunir no núcleo do app:

- `CitizenRecord`
- `CitizenProfileExtension`
- `AttendanceUnit`
- `ServiceCatalog`
- `QueueTicket`
- `ERPSecretariatMirror`
- `ERPDepartmentMirror`
- `ERPOperatorMirror`
- `OutboundSyncQueue`
- `IntegrationEventLog`

## 5. Comandos úteis

```bash
python manage.py migrate
python manage.py bootstrap_c2ta
python manage.py check_external_base
```
