# CHANGELOG JURÍDICO AMBIENTAL

Registro cronológico (mais recente primeiro) de novidades normativas, alterações, revogações, decisões
relevantes e CORREÇÕES da base. Cada entrada segue o bloco padrão. Nunca apagar entradas; corrigir com
nova entrada.

Bloco padrão:
```
## AAAA-MM-DD — <título curto>
- DATA: AAAA-MM-DD (da verificação) | DATA DO ATO: AAAA-MM-DD
- NORMA/JULGADO: identificação completa (ID da ficha quando houver)
- ALTERAÇÃO: o que mudou / o que foi registrado / o que foi corrigido
- IMPACTO: efeito prático
- ÁREA AFETADA: temas (licenciamento, flora, infrações...)
- PROCESSOS/CLIENTES POTENCIALMENTE AFETADOS: (preencher; sem dados pessoais)
- FONTE OFICIAL: URL | NÍVEL DE VERIFICAÇÃO: FONTE_PRIMARIA / INDIRETA / NAO_VERIFICADA
- RESPONSÁVEL: agente/comando que registrou
```

---

## 2026-09-11 — Ampliação territorial: perfis de 14 UFs e dossiês de Salvador, Simões Filho, Candeias e Teresina
- DATA: 2026-09-11 | DATA DO ATO: n/a
- NORMA/JULGADO: estadual/{sc,pr,sp,mg,mt,ms,go,rj,pe,pb,es,ce,ba,pi}/PERFIL.md + fichas (ver indices/por_uf.md); municipal/ba/{salvador,simoes_filho,candeias}.md; municipal/pi/teresina.md; agente direito-ambiental-estados
- ALTERAÇÃO: criados perfis estaduais (órgão licenciador, conselho, recursos hídricos, portal) e fichas das normas
  centrais confirmadas por WebSearch (INDIRETA) — inclusive revogações relevantes: GO Lei 8.544/1978 → Lei 20.694/2019;
  RJ Dec. 44.820/2014 → Dec. 46.890/2019; RJ CONEMA 42/2012 → CONEMA 92/2021. Normas lembradas sem confirmação ficaram
  NAO_VERIFICADA ou em PENDENTES (23-29).
- IMPACTO: habilita análise em 15 UFs; nenhum texto estadual foi lido — artigos não devem ser citados sem leitura.
- ÁREA AFETADA: competência; licenciamento; recursos hídricos; flora; infrações (estaduais)
- PROCESSOS/CLIENTES POTENCIALMENTE AFETADOS: projetos BA (RMS) e PI (Teresina)
- FONTE OFICIAL: URLs nas fichas | NÍVEL DE VERIFICAÇÃO: INDIRETA (predominante)
- RESPONSÁVEL: implantação (ampliação solicitada pelo usuário)

## 2026-09-11 — Criação do núcleo e carga inicial (seed)
- DATA: 2026-09-11 | DATA DO ATO: n/a
- NORMA/JULGADO: carga inicial de fichas federais, RS, municipais (dossiês), jurisprudência, temas
- ALTERAÇÃO: estrutura criada. Fichas seed marcadas majoritariamente como `NAO_VERIFICADA` (origem:
  conhecimento do modelo). Poucas fichas receberam `INDIRETA` a partir de WebSearch realizado nesta data.
- IMPACTO: a base funciona como ÍNDICE; nenhuma ficha `NAO_VERIFICADA` pode fundamentar manifestação
  relevante sem reverificação.
- ÁREA AFETADA: todas
- PROCESSOS/CLIENTES POTENCIALMENTE AFETADOS: n/a
- FONTE OFICIAL: n/a | NÍVEL DE VERIFICAÇÃO: NAO_VERIFICADA (regra geral do seed)
- RESPONSÁVEL: implantação inicial

## 2026-09-11 — Lei 15.190/2025 (Lei Geral do Licenciamento Ambiental) e derrubada de vetos
- DATA: 2026-09-11 | DATA DO ATO: 2025-08-08 (publicação); 2025-11-27 (derrubada de 52 vetos)
- NORMA/JULGADO: LEI-FED-15190-2025
- ALTERAÇÃO: registrada com status `ALTERADA` (texto promulgado após derrubada de vetos e MP 1.308/2025
  sobre LAE ainda não incorporados dispositivo a dispositivo na ficha). 63 vetos originais; 52 derrubados
  em 27/11/2025; vetos sobre Licença Ambiental Especial (LAE) não apreciados por serem objeto da MP 1.308/2025.
- IMPACTO: MUITO ELEVADO — altera o regime geral de licenciamento (tipos de licença, LAC, dispensas,
  prazos, competências). Toda análise de licenciamento deve verificar o texto vigente.
- ÁREA AFETADA: licenciamento; competência; infrações correlatas
- PROCESSOS/CLIENTES POTENCIALMENTE AFETADOS: todos os processos de licenciamento em curso
- FONTE OFICIAL: https://www2.camara.leg.br/legin/fed/lei/2025/lei-15190-8-agosto-2025-797833-publicacaooriginal-176089-pl.html ;
  https://www12.senado.leg.br/noticias/materias/2025/11/27/congresso-derruba-52-itens-de-veto-a-lei-geral-do-licenciamento-ambiental
  | NÍVEL DE VERIFICAÇÃO: INDIRETA (WebSearch; acesso direto bloqueado)
- RESPONSÁVEL: implantação inicial

## 2026-09-11 — Resolução CONSEMA 372/2018: alterações por CONSEMA 527/2025, 543/2026 e 544/2026
- DATA: 2026-09-11 | DATA DO ATO: 2025 (527); 2026-02-23 (543 e 544)
- NORMA/JULGADO: RES-CONSEMA-RS-372-2018; RES-CONSEMA-RS-527-2025; RES-CONSEMA-RS-543-2026; RES-CONSEMA-RS-544-2026
- ALTERAÇÃO: 527/2025 inclui no Anexo III atividades não incidentes de licenciamento (saneamento, data
  center, espuma — conforme título do PDF oficial). 543/2026 exclui "Silvicultura de Exóticas" do Anexo I
  (não incidência) e altera CODRAM 3510,52 e 10430,20 (linhas de transmissão acima de 138 kV). 544/2026
  repassa ao município a lavra de gemas a céu aberto porte pequeno (CODRAM 530,04) e cria CODRAM 3510,55
  (armazenamento de energia por baterias) sob competência estadual. SEMA publicou compilação em 2025-12.
- IMPACTO: ELEVADO — competência (Estado x município) e incidência de licenciamento no RS
- ÁREA AFETADA: licenciamento RS; competência; silvicultura; mineração; energia
- PROCESSOS/CLIENTES POTENCIALMENTE AFETADOS: enquadramentos CODRAM em curso na Serra Gaúcha
- FONTE OFICIAL: https://www.sema.rs.gov.br/resolucoes ;
  https://www.sema.rs.gov.br/upload/arquivos/202512/03160402-3722018-ultima-atualizacao-compilada.pdf ;
  https://www.sema.rs.gov.br/upload/arquivos/202505/19085550-resolucao-527-2025-altera-a-resolucao-3722018-saneamento-data-center-espuma.pdf
  | NÍVEL DE VERIFICAÇÃO: INDIRETA (WebSearch; conteúdo das 543/544 via fontes secundárias)
- RESPONSÁVEL: implantação inicial

## 2026-09-11 — ADPF 748 (CONAMA 500/2020) — mérito julgado; CONAMA 284, 302 e 303 restabelecidas
- DATA: 2026-09-11 | DATA DO ATO: 2021-12 (mérito, Plenário, unanimidade, Rel. Min. Rosa Weber)
- NORMA/JULGADO: STF-ADPF-748; RES-CONAMA-302-2002; RES-CONAMA-303-2002
- ALTERAÇÃO: CONAMA 303/2002 e 302/2002 registradas como `VIGENTE` (restabelecidas). CONAMA 500/2020
  declarada inconstitucional.
- IMPACTO: ELEVADO — parâmetros de APP (CONAMA 303) e reservatórios (302) permanecem aplicáveis no que
  não conflitar com a Lei 12.651/2012.
- ÁREA AFETADA: APP; licenciamento
- FONTE OFICIAL: https://noticias.stf.jus.br/postsnoticias/restabelecidas-normas-do-conama-sobre-areas-de-protecao-e-licenciamento/
  | NÍVEL DE VERIFICAÇÃO: INDIRETA
- RESPONSÁVEL: implantação inicial

## 2026-09-11 — ADI 7146 (Lei 14.285/2021 — APP urbana) — pendente de julgamento de mérito
- DATA: 2026-09-11 | DATA DO ATO: informação secundária datada de meados de 2025
- NORMA/JULGADO: STF-ADI-7146; LEI-FED-14285-2021
- ALTERAÇÃO: Lei 14.285/2021 registrada como `EFICACIA_QUESTIONADA`. Rel. Min. André Mendonça; sem
  cautelar apreciada; sem mérito até a última informação localizada. RECHECAR: fonte é de 2025; pode
  haver julgamento entre 2025-06 e 2026-09.
- IMPACTO: MUITO ELEVADO para loteamentos/APP urbana na Serra Gaúcha
- ÁREA AFETADA: APP urbana; urbanístico; parcelamento do solo
- FONTE OFICIAL: https://portal.stf.jus.br/ (processo ADI 7146) | NÍVEL DE VERIFICAÇÃO: INDIRETA (desatualizada)
- RESPONSÁVEL: implantação inicial

## 2026-09-11 — Decreto 11.373/2023 altera Decreto 6.514/2008 (conciliação revogada; conversão de multa)
- DATA: 2026-09-11 | DATA DO ATO: 2023-01-01
- NORMA/JULGADO: DEC-FED-6514-2008; DEC-FED-11373-2023
- ALTERAÇÃO: revogação dos dispositivos de conciliação ambiental (inseridos pelo Dec. 9.760/2019); pedido de
  conversão de multa até alegações finais; prazo de 60 dias para projeto de conversão; 50% das multas ao FNMA.
- IMPACTO: ELEVADO — processo administrativo federal (IBAMA/ICMBio)
- ÁREA AFETADA: infrações
- FONTE OFICIAL: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/decreto/D11373.htm (não acessada)
  | NÍVEL DE VERIFICAÇÃO: INDIRETA
- RESPONSÁVEL: implantação inicial

## 2026-09-11 — Farroupilha/RS — Decreto Municipal 7.901/2026 (procedimentos de licenciamento)
- DATA: 2026-09-11 | DATA DO ATO: 2026-09 (notícia de 2026-09-05)
- NORMA/JULGADO: dossiê municipal/rs/farroupilha.md
- ALTERAÇÃO: decreto municipal atualiza procedimentos de licenciamento alinhando-os à Lei 15.190/2025 e ao
  Decreto 10.936/2022; simplifica documentação; dispensa documentos de órgãos fora do SISNAMA.
- IMPACTO: MODERADO/ELEVADO para processos municipais em Farroupilha
- ÁREA AFETADA: licenciamento municipal
- FONTE OFICIAL: https://farroupilha.rs.gov.br/ (texto do decreto não acessado) | NÍVEL DE VERIFICAÇÃO: INDIRETA (notícias locais)
- RESPONSÁVEL: implantação inicial
