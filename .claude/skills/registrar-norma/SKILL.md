---
name: registrar-norma
description: "Cadastra ou atualiza uma ficha de norma, julgado ou município na base do NUCLEO_DIREITO_AMBIENTAL sem duplicar, preenchendo o frontmatter padrão, o nível de verificação e o CHANGELOG, e regenerando os índices. Use quando o usuário fornecer uma norma/decisão (texto, PDF, link) ou quando uma pesquisa identificar norma ainda não cadastrada."
argument-hint: "<tipo: norma|julgado|municipio> <identificação (ex.: Lei 12.651/2012; REsp 1.770.760; Caxias do Sul/RS)> [caminho do texto oficial ou URL]"
---

# /registrar-norma — cadastro sem duplicação

Entrada: **$ARGUMENTS**

1. **Verificar duplicidade**: `grep -ril "<número>" direito_ambiental/{federal,estadual,municipal,jurisprudencia}`
   e `indices/normas.json`. Se existir ficha → ATUALIZAR (não criar outra).
2. **Fonte**: se o usuário forneceu texto/PDF → nível `FONTE_PRIMARIA`, método `documento_fornecido_usuario`
   (guardar URL/origem). Se só URL oficial acessível → WebFetch → `FONTE_PRIMARIA`. Se só WebSearch → `INDIRETA`.
   Se nada → `NAO_VERIFICADA` e a ficha declara isso.
3. **Criar/atualizar** a partir de `direito_ambiental/templates/FICHA_NORMA.md` / `FICHA_JULGADO.md` /
   `MUNICIPIO.md`. ID no padrão do template. Dispositivos: redação entre aspas SOMENTE se conferida.
   Preencher `alterada_por`/`revogada_por`/`altera`/`revoga` e criar/atualizar as fichas relacionadas
   (ex.: ao cadastrar norma revogadora, marcar a revogada como REVOGADA).
4. **Vocabulário**: usar assuntos de `direito_ambiental/indices/VOCABULARIO.md` (adicionar termo novo lá se preciso).
5. **CHANGELOG** se for novidade/alteração/revogação/correção.
6. `python3 direito_ambiental/scripts/gerar_indices.py && python3 direito_ambiental/scripts/validar_base.py`.
7. Informar ao usuário: arquivo criado/atualizado, nível de verificação, pendências.
