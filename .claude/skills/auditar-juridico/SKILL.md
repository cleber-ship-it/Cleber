---
name: auditar-juridico
description: Auditoria jurídica adversarial de um documento (parecer, defesa, recurso, laudo com fundamentação legal, minuta de TAC/TC, resposta a notificação, relatório técnico). Analisa o texto integralmente procurando citação incorreta, artigo inexistente, norma revogada, interpretação excessiva, jurisprudência superada ou não identificada, inconsistência lógica, risco jurídico não declarado, confusão entre texto legal e interpretação, e argumentos adversos não enfrentados. Produz relatório de achados com gravidade e correção sugerida.
argument-hint: <caminho do arquivo (md, txt, docx, pdf) ou texto colado>
---

# /auditar-juridico — auditoria de documento

Alvo: **$ARGUMENTS**

## 1. Carregar o documento
Se for caminho: leia integralmente (docx/pdf → extraia texto com as ferramentas disponíveis). Se for texto
colado, use-o. Numere parágrafos/trechos para localização dos achados.

## 2. Extrair todas as citações
Liste TODAS as referências a normas (tipo, número, ano, artigo, §, inciso, redação transcrita) e a julgados
(tribunal, classe, número, relator, data, tese) e todas as afirmações do tipo "a lei exige", "é obrigatório",
"o STJ entende", "conforme a resolução".

## 3. Verificar cada citação
Acione `verificador-fontes-normativas` com a lista completa. Para cada: existe? vigente? redação confere?
alterada? URL? nível de verificação. Cruze com `direito_ambiental/indices/normas.json` e fichas.

## 4. Análise substantiva (em paralelo)
- `revisor-juridico-adversarial`: ataques ao documento (argumentos adversos não enfrentados, exceções,
  competência, conflito normativo, precedentes contrários).
- Especialistas temáticos pertinentes: interpretação excessiva? texto x interpretação confundidos?
  obrigação x recomendação confundidas? competência?
- `jurisprudencia-ambiental`: precedentes citados — autênticos? superados? distinguíveis? força real?

## 5. Consistência lógica e risco
Verifique: premissas → conclusão; contradições internas; premissas técnicas não fundamentadas; ausência de
classificação de risco/confiança; datas de corte; hierarquia normativa presumida.

## 6. Relatório
Use `direito_ambiental/templates/AUDITORIA.md`: sumário por gravidade; tabela de achados (trecho, problema,
tipo, gravidade, evidência com nível de verificação, correção sugerida); citações não verificáveis nesta
auditoria; risco global do documento. Seja crítico e específico; não suavize achados CRÍTICOS.

## 7. Registro
Grave o relatório em `direito_ambiental/memoria/pesquisas/PESQ-<data>-auditoria-<slug>.md`, indexe em
`memoria/INDICE.md`. Se a auditoria revelar erro em ficha da base, corrija a ficha e registre no
CHANGELOG (regra 11 do CLAUDE.md). Não altere o documento auditado sem pedido expresso.
