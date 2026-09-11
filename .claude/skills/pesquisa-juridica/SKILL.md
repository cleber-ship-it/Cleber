---
name: pesquisa-juridica
description: Pesquisa jurídica ambiental PROFUNDA para temas de maior relevância — investigação ampliada em legislação (federal/RS/municipal), regulamentos, jurisprudência (STF/STJ/TRF4/TJRS), decisões administrativas, doutrina quando útil, histórico legislativo e alterações posteriores, com verificação de fontes, revisão adversarial e registro em memória. Use quando a resposta rápida do /direito-ambiental não basta ou quando o tema embasará parecer, defesa, recurso, TAC ou manifestação formal.
argument-hint: <tema ou questão; contexto fático; município/UF; atividade; finalidade (parecer, defesa, etc.)>
---

# /pesquisa-juridica — investigação ampliada

Objeto: **$ARGUMENTS**

Siga `direito_ambiental/PROTOCOLO_PESQUISA.md` integralmente (16 passos). Diferenças em relação ao
`/direito-ambiental`:

1. **Triagem** (`coordenador-direito-ambiental`) com plano de pesquisa explícito: lista de normas a
   localizar por ente, julgados a autenticar, decisões administrativas/notas técnicas a procurar, histórico
   legislativo (redação original → alterações → projetos em tramitação relevantes).
2. **Atualização prévia obrigatória**: `verificador-fontes-normativas` reverifica TODAS as fichas centrais
   do tema antes da análise (não só as vencidas). Acesso direto bloqueado → WebSearch + INDIRETA, declarado.
3. **Especialistas** (todos os pertinentes) + `jurisprudencia-ambiental` obrigatório, com busca de
   precedentes CONTRÁRIOS e verificação de superação/distinção.
4. **Histórico legislativo e alterações**: montar linha do tempo da(s) norma(s) central(is) (redações,
   ADIs, MPs, vetos), indicando o texto aplicável à data do fato (tempus regit actum) e à data atual.
5. **Doutrina** apenas quando ajude a interpretar; nunca como substituto de norma/precedente; citar autor/obra.
6. **Revisão adversarial** (`revisor-juridico-adversarial`) — obrigatória; repetir se a consolidação mudar a tese.
7. **Produto**: relatório em `direito_ambiental/memoria/pesquisas/PESQ-<data>-<slug>.md` com: resposta no
   formato padrão; linha do tempo; tabela de normas (id, dispositivo, status, verificação); tabela de
   julgados (identificação completa, força, situação); matriz de caso (`templates/MATRIZ_CASO.md`) se houver
   fato concreto; estratégia (`templates/ESTRATEGIA_JURIDICA.md`) se a finalidade for defesa/recurso/parecer;
   lacunas e gatilhos de reverificação. Indexar em `memoria/INDICE.md`.
8. **Base**: criar/atualizar fichas (sem duplicar), registrar novidades no CHANGELOG, rodar
   `gerar_indices.py` e `validar_base.py`.

Entregue ao usuário o relatório completo (não só um resumo) e informe o caminho do arquivo gravado.
