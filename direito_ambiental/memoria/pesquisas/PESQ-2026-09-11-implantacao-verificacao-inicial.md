---
tipo_registro: pesquisa
id: PESQ-2026-09-11-IMPLANTACAO-VERIFICACAO-INICIAL
data: 2026-09-11
comando: /atualizar-direito-ambiental (implantação do núcleo)
questao: "Verificação inicial, via WebSearch, dos pontos de maior risco de desatualização do conhecimento do modelo: Lei Geral do Licenciamento; CONSEMA 372/2018; ADPF 748; ADI 7146; Código Estadual RS; Dec. 6.514; legislação de Farroupilha."
territorio: "FEDERAL / RS / Farroupilha-RS"
atividade: "transversal"
temas: [licenciamento, competencia, app, infracoes]
normas_citadas: [LEI-FED-15190-2025, RES-CONSEMA-RS-372-2018, RES-CONSEMA-RS-527-2025, RES-CONSEMA-RS-543-2026, RES-CONSEMA-RS-544-2026, LEI-FED-14285-2021, LEI-RS-15434-2020, LEI-RS-11520-2000, LEI-RS-9519-1992, DEC-FED-6514-2008, DEC-FED-11373-2023, RES-CONAMA-302-2002, RES-CONAMA-303-2002]
julgados_citados: [STF-ADPF-748, STF-ADI-7146]
resposta_direta: "Confirmadas indiretamente 7 novidades/alterações relevantes; nenhuma fonte primária pôde ser lida (bloqueio de rede)."
confianca: MEDIA
risco: ELEVADO
nivel_verificacao_predominante: INDIRETA
revisao_adversarial: false
validade_estimada: 2026-10-11
---

# Verificação inicial de pontos críticos (implantação, 2026-09-11)

## Contexto
Na criação do núcleo testou-se o acesso a fontes: curl e WebFetch retornaram EGRESS_BLOCKED/403 para
planalto.gov.br, camara.leg.br, stf.jus.br, stj.jus.br, al.rs.gov.br, sema.rs.gov.br, fepam.rs.gov.br,
conama.mma.gov.br e legisweb.com.br. WebSearch funcionou. Logo, o nível máximo desta rodada é INDIRETA.

## Achados (todos INDIRETA — fontes secundárias/notícias oficiais via WebSearch)
| # | Achado | Fonte localizada | Impacto |
|---|---|---|---|
| 1 | Lei 15.190/2025 (Lei Geral do Licenciamento): publicada 08/08/2025 com 63 vetos; 52 vetos derrubados em 27/11/2025; vetos sobre LAE ficaram para a MP 1.308/2025 | Senado Notícias (2025-08-08; 2025-11-27); Câmara LEGIN; MPPR; LexLegal | MUITO ELEVADO — regime geral de licenciamento mudou; texto consolidado não lido |
| 2 | CONSEMA 372/2018 alterada por 527/2025 (Anexo III — não incidência: saneamento, data center, espuma), 543/2026 (silvicultura de exóticas não incidente; LTs >138 kV) e 544/2026 (gemas porte pequeno → município; CODRAM 3510,55 baterias); compilação SEMA 2025-12 | sema.rs.gov.br (títulos de PDFs); LegisWeb; DPM; Silveiro | ELEVADO — competência e incidência no RS |
| 3 | ADPF 748: mérito julgado (dez/2021), CONAMA 500/2020 inconstitucional; CONAMA 284/302/303 restabelecidas | noticias.stf.jus.br; PDF adpf748 | ELEVADO — parâmetros de APP |
| 4 | ADI 7146 (Lei 14.285/2021): pendente, Rel. André Mendonça, sem cautelar (informação de 2025) | escritórios; NT Conjunta CAOMA-CAOURB MPRS 01/2024 | MUITO ELEVADO — APP urbana; informação possivelmente desatualizada |
| 5 | Lei 15.434/2020 (Código Estadual RS) revogou integralmente a Lei 11.520/2000 e artigos da Lei 9.519/1992 | SEMA (PDF); Famurs; Souto Correa | ELEVADO |
| 6 | Dec. 11.373/2023 alterou o Dec. 6.514/2008: revogou conciliação; conversão de multa até alegações finais; 60 dias para projeto; 50% ao FNMA | ConJur; Mattos Filho; Milaré | ELEVADO — processo federal |
| 7 | Farroupilha/RS: Secretaria de Urbanismo e Meio Ambiente licencia; Dec. Municipal 7.901/2026 alinha procedimentos à Lei 15.190/2025 e Dec. 10.936/2022 | farroupilha.rs.gov.br; Leouve; Spaço FM (2026-09-05) | MODERADO/ELEVADO |

## Fontes consultadas (URLs)
- https://www12.senado.leg.br/noticias/materias/2025/08/08/publicada-lei-do-licenciamento-ambiental-com-63-vetos
- https://www12.senado.leg.br/noticias/materias/2025/11/27/congresso-derruba-52-itens-de-veto-a-lei-geral-do-licenciamento-ambiental
- https://www2.camara.leg.br/legin/fed/lei/2025/lei-15190-8-agosto-2025-797833-publicacaooriginal-176089-pl.html
- https://www.sema.rs.gov.br/upload/arquivos/202512/03160402-3722018-ultima-atualizacao-compilada.pdf
- https://www.sema.rs.gov.br/upload/arquivos/202505/19085550-resolucao-527-2025-altera-a-resolucao-3722018-saneamento-data-center-espuma.pdf
- https://www.legisweb.com.br/legislacao/?id=491086 (CONSEMA 543/2026)
- https://noticias.stf.jus.br/postsnoticias/restabelecidas-normas-do-conama-sobre-areas-de-protecao-e-licenciamento/
- https://www.cnmp.mp.br/portal/images/CMA/arquivos/MPRS/6_nt_caoma_caurb_01_2024_lf_14285_2021_apps_vf.pdf
- https://www.sema.rs.gov.br/upload/arquivos/202306/13094545-codigo-estadual-do-meio-ambiente-lei-15434-2020.pdf
- https://www.conjur.com.br/2023-jan-20/bruno-kryminice-infracoes-ambientais-decreto-113732023/
- https://farroupilha.rs.gov.br/secretaria/id/1011/ ; https://leouve.com.br/meio-ambiente/farroupilha-atualiza-procedimentos-para-licenciamento-ambiental/

## Revisão adversarial
Não executada (rodada de verificação de fontes, sem conclusão jurídica de mérito).

## Gatilhos de reverificação
- Qualquer manifestação sobre licenciamento → ler texto consolidado da Lei 15.190/2025 e MP 1.308/2025.
- Qualquer manifestação sobre APP urbana → checar andamento da ADI 7146.
- Enquadramento CODRAM → abrir compilação vigente da CONSEMA 372 (pós-fev/2026).
