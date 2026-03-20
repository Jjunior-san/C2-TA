# Próximos passos dos modelos do C2-TA

## Arquivos já adicionados

- `triagem/models.py`
- `triagem/integration_models.py`
- `triagem/citizen_profile.py`

## Objetivo

Esses arquivos preparam o C2-TA para:

- cadastro local de cidadãos
- deploy separado
- integração com o ERP C²
- fila de sincronização
- espelho de secretarias, departamentos e operadores

## Próxima consolidação

Na próxima etapa, integrar esses arquivos ao núcleo do app:

1. importar os novos modelos no carregamento principal
2. registrar no admin
3. gerar migrations
4. criar rotinas de sincronização com o ERP
5. ligar o cadastro de cidadão à emissão de senha

## Direção funcional

- `CitizenRecord` continua sendo o cadastro principal local
- `CitizenProfileExtension` complementa os dados de cidadão para integração futura
- `ERPSecretariatMirror`, `ERPDepartmentMirror` e `ERPOperatorMirror` servem como espelho institucional
- `OutboundSyncQueue` e `IntegrationEventLog` garantem tolerância a falhas do ERP
