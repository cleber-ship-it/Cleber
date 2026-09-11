---
name: atualizar-direito-ambiental
description: Rotina de atualização do NUCLEO_DIREITO_AMBIENTAL. Pesquisa novas leis, leis complementares, decretos, resoluções CONAMA/CNRH, normas IBAMA/ICMBio, alterações legislativas, decisões STF/STJ, legislação ambiental do RS (CONSEMA, FEPAM, SEMA, DRHS) e dos municípios cadastrados; compara com a última atualização; registra APENAS novidades, alterações, revogações e decisões relevantes no CHANGELOG; atualiza fichas, status de vigência, datas de verificação, STATUS.md e índices. Use mensalmente ou antes de manifestações relevantes.
argument-hint: [escopo opcional: federal | rs | municipal | jurisprudencia | tema:<nome> | id:<ID> | tudo]
---

# /atualizar-direito-ambiental — rotina de atualização

Escopo: **$ARGUMENTS** (vazio = tudo)

## 0. Preparação
Leia `direito_ambiental/STATUS.md` (última atualização), `direito_ambiental/CHANGELOG_JURIDICO_AMBIENTAL.md`
(entradas desde então), `direito_ambiental/PENDENTES_DE_LEVANTAMENTO.md` e rode
`python3 direito_ambiental/scripts/validar_base.py --vencidas` para listar fichas com verificação vencida.
Teste o acesso: tente WebFetch em uma URL oficial; se bloqueado, toda a rotina registra nível INDIRETA e
isso é dito no relatório final.

## 1. Frentes de pesquisa (acionar `verificador-fontes-normativas` em paralelo por frente, com a janela
temporal "desde <última atualização>")
1. Federal — leis e LCs novas/alteradas (Planalto/Senado/Câmara; WebSearch "lei ambiental <ano>", "altera a Lei 12.651", "altera a Lei 9.605", "Lei 15.190 regulamento", "MP 1.308").
2. Federal — decretos (Dec. 6.514, 6.660, 10.936, regulamentos da Lei 15.190).
3. CONAMA e CNRH — novas resoluções e revogações.
4. IBAMA / ICMBio — INs e portarias (SINAFLOR, DOF, conversão de multas, fauna, UCs).
5. STF — ADIs/ADPFs/temas ambientais (ADI 7146; Código Florestal; competência; Lei 15.190 se impugnada).
6. STJ — súmulas novas, temas repetitivos ambientais, teses da 1ª Seção.
7. RS — leis e decretos (AL-RS), CONSEMA (nova compilação da 372/2018; resoluções novas), FEPAM/SEMA portarias, CRH/DRHS.
8. Municípios cadastrados em `direito_ambiental/municipal/` — leis, decretos, resoluções de conselho.
9. Itens de `PENDENTES_DE_LEVANTAMENTO.md` (tentar resolver; mover para ficha ou refutar).

## 2. Comparação
Para cada achado: já está na base? (grep por número/ID em `indices/normas.json` e fichas). Se sim e nada
mudou → só atualizar `verificacao.data_ultima_verificacao` via `registrar_verificacao.py`. Se mudou →
atualizar ficha (status, alterada_por, revogada_por, dispositivos), registrar no CHANGELOG.
Se novo → criar ficha pelo template (sem duplicar) + CHANGELOG.

## 3. Registro (APENAS novidades, alterações, revogações, decisões relevantes)
CHANGELOG com o bloco padrão (DATA, NORMA, ALTERAÇÃO, IMPACTO, ÁREA AFETADA, PROCESSOS/CLIENTES
POTENCIALMENTE AFETADOS, FONTE OFICIAL + nível de verificação). Para "processos/clientes afetados", cruzar
com `memoria/INDICE.md` (temas/territórios das pesquisas anteriores) e listar os IDs de pesquisa afetados.

## 4. Fechamento
- Atualizar `STATUS.md` (data, próxima atualização, prioridades abertas, limitação de acesso).
- `python3 direito_ambiental/scripts/gerar_indices.py && python3 direito_ambiental/scripts/validar_base.py`.
- Reverificar pesquisas em `memoria/` cuja `validade_estimada` venceu ou cujos temas foram afetados: marcar
  no arquivo a necessidade de reverificação (não apagar histórico).
- Relatório final ao usuário: novidades (tabela), fichas atualizadas, fichas ainda NAO_VERIFICADA críticas,
  limitações de acesso encontradas.
