# Protocolo de integração núcleo jurídico ↔ agentes técnicos

## Princípio
Problema jurídico que depende de conceito técnico: **NÃO inventar a premissa técnica** — consultar o
especialista. Problema técnico cuja conclusão depende de interpretação normativa: **NÃO interpretar a
norma por conta própria** — consultar o núcleo jurídico.

## Áreas técnicas previstas e pontos típicos de interface
| Área | Perguntas típicas do jurídico ao técnico | Perguntas típicas do técnico ao jurídico |
|---|---|---|
| Biologia / Botânica | estágio sucessional (Mata Atlântica, CONAMA 33/1994 no RS); espécies ameaçadas/imunes de corte; fitofisionomia; exótica invasora | limites de supressão por estágio; compensação exigida; autorização competente |
| Fauna | ocorrência, impacto, resgate, soltura | licenças de manejo; infrações (Lei 9.605 arts. 29-37) |
| Engenharia ambiental / sanitária / química | parâmetros de efluente/emissão; classificação de resíduo; contaminação | padrões legais aplicáveis (CONAMA 357/430, CONSEMA 355); enquadramento de resíduo (PNRS) |
| Hidrologia / hidrogeologia | largura de curso d'água; regime (perene/intermitente/efêmero); nascente; vazão; recarga | metragem de APP; outorga/dispensa; enquadramento do corpo hídrico |
| Geologia | declividade (>45°), topo de morro, encosta, área de risco, minério | APP de declividade/topo; competência de licenciamento mineral (ANM x órgão ambiental) |
| SIG / Geoprocessamento / Topografia | área (ha), perímetro, sobreposição a APP/UC/zona urbana, uso consolidado em 22/07/2008 | área rural consolidada (Lei 12.651 art. 3º IV); área urbana consolidada (Lei 12.651 art. 3º XXVI; Lei 6.766 art. 2º; Lei 14.285) |
| Urbanismo / Engenharia civil | infraestrutura existente; densidade; zoneamento gráfico | requisitos da Lei 6.766; plano diretor; REURB |

## Formato `CONSULTA_TECNICA` (jurídico → técnico)
```
CONSULTA_TECNICA
- Caso/ID:
- Premissa que preciso confirmar: (ex.: "o fragmento suprimido estava em estágio médio de regeneração")
- Por que importa juridicamente: (ex.: define incidência do art. 14 da Lei 11.428/2006)
- Evidência disponível: (laudo, fotos, imagens, campo)
- Grau de certeza necessário: (indicativo / pericial)
```
## Formato `RESPOSTA_TECNICA` (técnico → jurídico)
```
RESPOSTA_TECNICA
- Premissa: CONFIRMADA / REFUTADA / INDETERMINADA
- Método/critério técnico usado: (ex.: parâmetros da CONAMA 33/1994: altura média, DAP, serapilheira...)
- Dados: 
- Incerteza: 
- O que confirmaria/refutaria com mais segurança:
```
## Formato `CONSULTA_JURIDICA` (técnico → jurídico)
```
CONSULTA_JURIDICA
- Contexto técnico:
- Pergunta normativa: (ex.: "qual a largura de APP para curso d'água de 8 m em zona urbana de Farroupilha?")
- Território / atividade:
- Urgência:
```
A resposta jurídica segue `templates/RESPOSTA_JURIDICA.md`, sempre com CONFIANÇA e DATA DAS FONTES.

## Registro
Consultas cruzadas relevantes são anotadas na ficha de pesquisa (`memoria/pesquisas/`) no campo
"Premissas técnicas".

## Agentes técnicos existentes nesta base
Em 2026-09-11 não havia agentes técnicos especializados; foi criado um consultor técnico GENÉRICO. Agentes
especializados por área devem ser criados com `templates/AGENTE_TECNICO.md` e registrados aqui (o genérico passa a
encaminhar para eles):
| Agente | Arquivo | Área | Criado em |
|---|---|---|---|
| `consultor-tecnico-ambiental` (GENÉRICO — substituto até existirem especialistas) | `.claude/agents/consultor-tecnico-ambiental.md` | todas as áreas da tabela acima | 2026-09-11 |
