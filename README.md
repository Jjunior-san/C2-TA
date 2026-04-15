# C2-TA

Sistema de **Triagem e Atendimento** da C2 Sistemas.

## Objetivo

O C2-TA será um módulo voltado para:

- emissão de senhas
- triagem inicial
- gestão de filas
- chamada em painel
- atendimento em guichê
- encaminhamento interno
- integração com suporte, agenda e estrutura administrativa

## Direção técnica

Base planejada em:

- Python
- Django
- PostgreSQL

## Arquitetura prevista

O projeto deverá operar com base unificada e integração com o ecossistema C2, reaproveitando entidades administrativas, usuários, setores e fluxos de atendimento.

## Próximos passos

1. Estruturar o app Django inicial
2. Criar modelos de triagem e atendimento
3. Implementar emissão de senha
4. Implementar painel de chamadas
5. Implementar relatórios operacionais

## Deploy no Portainer

- Para stack com build local no host/engine: `stack.portainer.yml`
- Para stack criada pelo modo **Git repository** do Portainer: `stack.portainer.git.yml`
