# Integração C2-TA ↔ ERP C²

## Princípio

- deploy separado
- banco separado
- ecossistema integrado
- comunicação por API, token e webhook

## ERP é mestre de

- secretarias
- departamentos
- operadores
- chamados institucionais
- agenda

## C2-TA é mestre de

- cidadãos
- senhas
- triagem
- fila
- atendimento presencial
- chamadas no painel

## Dados que o C2-TA consulta do ERP

- secretariats
- departments
- employees

## Dados que o C2-TA envia ao ERP

- resumo do atendimento
- abertura de chamado
- criação de retorno/agendamento
- vínculo institucional do atendimento

## Endpoints previstos no ERP

- GET /api/integration/secretariats/
- GET /api/integration/departments/
- GET /api/integration/employees/
- POST /api/integration/support-tickets/
- POST /api/integration/calendar-events/
- POST /api/integration/attendance-events/

## Campos de integração sugeridos no C2-TA

- erp_secretariat_id
- erp_department_id
- erp_employee_id
- erp_user_id
- erp_support_ticket_id
- erp_calendar_event_id
- external_reference
- source_system
- sync_status
- last_synced_at

## Estratégia de sincronização

### ERP -> C2-TA

Sincronização periódica de cadastros institucionais.

### C2-TA -> ERP

Envio quase em tempo real de eventos operacionais.

## Regras

1. Não depender de join entre bancos.
2. Sempre trafegar external_reference.
3. Atendimento presencial precisa continuar operando mesmo se o ERP estiver fora.
4. Eventos pendentes devem entrar em fila local para reenvio.
