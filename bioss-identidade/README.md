# BIOSS — Identidade Visual

Manual de identidade visual do BIOSS, aplicativo de gestão de licenças, prazos e
protocolos ambientais da Biogênese Licenciamento Ambiental.

O PDF não é editado à mão: ele é **gerado** a partir de `tokens.json`. Alterou uma
cor, uma medida ou uma escala, altere no token e reconstrua.

## Gerar

```
python3 build.py
```

Sem dependências de terceiros. Precisa apenas de Python 3 e Chromium instalado —
o script procura o binário em `CHROMIUM_CANDIDATOS`.

Saída: `dist/BIOSS-Identidade-Visual.pdf`, 13 páginas, A4 paisagem.

## Estrutura

| Caminho | O que é |
|---|---|
| `tokens.json` | Fonte única da verdade: cores, tipografia, geometria do símbolo, pares de contraste obrigatórios |
| `build.py` | Desenha o símbolo, monta o HTML com as fontes embutidas, renderiza o PDF |
| `assets/fonts/` | Outfit, Work Sans e IBM Plex Mono — todas sob OFL 1.1, licenças inclusas |
| `dist/` | O PDF gerado |
| `src/manual.html` | HTML intermediário (artefato de build, não versionado) |

## Trava de acessibilidade

Antes de gerar o PDF, o build confere todos os pares declarados em
`acessibilidade.pares_obrigatorios` contra a WCAG 2.1 — 4,5:1 para texto pequeno,
3:1 para elemento gráfico. **Se algum par reprovar, o build falha e não produz PDF.**

Foi assim que a paleta chegou à forma atual: o âmbar original (`#C98A22`) dava
2,94:1 com texto branco e foi reprovado; virou `#96631A`, com 5,13:1.

## O símbolo

Anéis concêntricos com centros deslocados 1,5 unidade da grade cada, e o anel
externo aberto entre 20° e 70°. Lê-se ao mesmo tempo como anel de crescimento de
árvore e como anel de progresso — o prazo que ainda não fechou.

Toda a geometria sai de `tokens.json` → `simbolo()`, sobre grade de 120 × 120.
Não há arquivo de logo a manter em sincronia: o símbolo é desenhado em código,
inclusive a versão simplificada para tamanhos abaixo de 24 px.

## Aberto nesta versão

- **Limiares de prazo** do sistema de estado (60 / 30 dias) são proposta — confirmar
  com a operação antes de codificar no app.
- **A sigla BIOSS** não tem expansão definida. O manual trata o nome como palavra,
  não como acrônimo. Se houver expansão oficial, ela entra na página de assinaturas.
