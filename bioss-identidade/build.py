#!/usr/bin/env python3
"""
Produção do manual de identidade visual do BIOSS.

    python3 build.py

Lê tokens.json, desenha o símbolo a partir da grade, monta o HTML com as fontes
embutidas e renderiza o PDF pelo Chromium. Nenhuma dependência externa.
"""

import base64
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).parent
FONTES = RAIZ / "assets" / "fonts"
SRC = RAIZ / "src"
DIST = RAIZ / "dist"

CHROMIUM_CANDIDATOS = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    "chromium",
    "chromium-browser",
    "google-chrome",
]


# ---------------------------------------------------------------- utilidades

def achar_chromium():
    for c in CHROMIUM_CANDIDATOS:
        if Path(c).exists():
            return c
        achado = shutil.which(c)
        if achado:
            return achado
    raise SystemExit("Chromium não encontrado. Instale o Chromium ou ajuste CHROMIUM_CANDIDATOS.")


def fonte_embutida(arquivo):
    dados = base64.b64encode((FONTES / arquivo).read_bytes()).decode()
    return f"data:font/ttf;base64,{dados}"


def rgb(hexa):
    h = hexa.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(hexa):
    def canal(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb(hexa))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    claro, escuro = max(la, lb), min(la, lb)
    return (claro + 0.05) / (escuro + 0.05)


# ------------------------------------------------------------------- símbolo

def ponto(cx, cy, r, ang):
    """Ângulo em graus, medido no sentido horário a partir das 12 horas."""
    rad = math.radians(ang)
    return cx + r * math.sin(rad), cy - r * math.cos(rad)


def arco(cx, cy, r, ini, fim):
    x1, y1 = ponto(cx, cy, r, ini)
    x2, y2 = ponto(cx, cy, r, fim)
    varredura = (fim - ini) % 360
    grande = 1 if varredura > 180 else 0
    return f"M {x1:.3f} {y1:.3f} A {r} {r} 0 {grande} 1 {x2:.3f} {y2:.3f}"


def simbolo(tokens, cor="#0E3B32", tamanho=120, classe="", simplificado=False):
    """
    Anel de crescimento: anéis concêntricos deslocados, o externo em abertura.
    Em `simplificado` reduz a dois anéis, para uso abaixo de 24 px.
    """
    s = tokens["simbolo"]
    grid = s["grid"]
    aneis = s["aneis"]
    if simplificado:
        aneis = [aneis[0], aneis[3]]

    partes = []
    for a in aneis:
        cx, cy = a["centro"]
        if a.get("preenchido"):
            partes.append(f'<circle cx="{cx}" cy="{cy}" r="{a["raio"]}" fill="{cor}"/>')
        elif a.get("aberto"):
            d = arco(cx, cy, a["raio"], a["gap_fim"], a["gap_inicio"])
            partes.append(
                f'<path d="{d}" fill="none" stroke="{cor}" '
                f'stroke-width="{a["traco"]}" stroke-linecap="round"/>'
            )
        else:
            partes.append(
                f'<circle cx="{cx}" cy="{cy}" r="{a["raio"]}" fill="none" '
                f'stroke="{cor}" stroke-width="{a["traco"]}"/>'
            )

    cls = f' class="{classe}"' if classe else ""
    return (
        f'<svg{cls} width="{tamanho}" height="{tamanho}" viewBox="0 0 {grid} {grid}" '
        f'xmlns="http://www.w3.org/2000/svg">{"".join(partes)}</svg>'
    )


def logotipo(tokens, cor="#0E3B32", altura=48, orientacao="horizontal", descritor=False):
    """Assinatura: símbolo + tipo. O descritor curto cabe em uma linha sob o tipo."""
    marca = tokens["marca"]
    texto_desc = marca["descritor_curto"]
    if orientacao == "horizontal":
        desc = (
            f'<div class="lk-desc" style="color:{cor}">{texto_desc}</div>'
            if descritor else ""
        )
        return f"""
        <div class="lockup lk-h">
          {simbolo(tokens, cor, altura)}
          <div class="lk-txt">
            <div class="lk-nome" style="color:{cor};font-size:{altura * 0.72:.1f}px">BIOSS</div>
            {desc}
          </div>
        </div>"""
    desc = (
        f'<div class="lk-desc lk-desc-c" style="color:{cor}">{texto_desc}</div>'
        if descritor else ""
    )
    return f"""
    <div class="lockup lk-v">
      {simbolo(tokens, cor, altura)}
      <div class="lk-nome" style="color:{cor};font-size:{altura * 0.62:.1f}px">BIOSS</div>
      {desc}
    </div>"""


# ----------------------------------------------------------------------- CSS

def css(tokens):
    d = tokens["documento"]
    faces = "\n".join([
        f"""@font-face{{font-family:'Outfit';font-weight:400;src:url('{fonte_embutida("Outfit-Regular.ttf")}')format('truetype')}}""",
        f"""@font-face{{font-family:'Outfit';font-weight:700;src:url('{fonte_embutida("Outfit-Bold.ttf")}')format('truetype')}}""",
        f"""@font-face{{font-family:'Work Sans';font-weight:400;src:url('{fonte_embutida("WorkSans-Regular.ttf")}')format('truetype')}}""",
        f"""@font-face{{font-family:'Work Sans';font-weight:700;src:url('{fonte_embutida("WorkSans-Bold.ttf")}')format('truetype')}}""",
        f"""@font-face{{font-family:'Work Sans';font-style:italic;src:url('{fonte_embutida("WorkSans-Italic.ttf")}')format('truetype')}}""",
        f"""@font-face{{font-family:'Plex Mono';font-weight:400;src:url('{fonte_embutida("IBMPlexMono-Regular.ttf")}')format('truetype')}}""",
        f"""@font-face{{font-family:'Plex Mono';font-weight:700;src:url('{fonte_embutida("IBMPlexMono-Bold.ttf")}')format('truetype')}}""",
    ])

    # As variáveis de cor vêm de tokens.json — nenhum valor é repetido aqui.
    apelidos = {
        "verde-profundo": "verde", "verde-vivo": "vivo", "verde-folha": "folha",
        "musgo": "musgo", "tinta": "tinta", "grafite": "grafite",
        "nevoa": "nevoa", "papel": "papel", "branco": "branco",
    }
    vars_cor = []
    for grupo in ("institucional", "neutro"):
        for c in tokens["cor"][grupo]:
            if c["id"] in apelidos:
                vars_cor.append(f'--{apelidos[c["id"]]}:{c["hex"]}')
    for c in tokens["cor"]["funcional"]:
        vars_cor.append(f'--{c["id"]}:{c["hex"]}')
    vars_cor.append("--nevoa-fria:#8FAFA1")   # texto secundário sobre fundo escuro
    vars_cor.append("--descritor:#9FBDB0")    # descritor sobre fundo escuro

    return f"""
{faces}

:root{{
  {"; ".join(vars_cor)};
  --m:{d["margem_mm"]}mm;
}}

*{{box-sizing:border-box;margin:0;padding:0}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:'Work Sans',sans-serif;color:var(--tinta);background:var(--papel)}}

@page{{size:{d["largura_mm"]}mm {d["altura_mm"]}mm;margin:0}}

.page{{
  width:{d["largura_mm"]}mm;height:{d["altura_mm"]}mm;
  position:relative;overflow:hidden;background:var(--papel);
  page-break-after:always;break-after:page;
}}
.page:last-child{{page-break-after:auto;break-after:auto}}
.page.escura{{background:var(--verde);color:var(--nevoa)}}

/* --- estrutura de página --- */
.cab{{
  position:absolute;top:var(--m);left:var(--m);right:var(--m);
  display:flex;justify-content:space-between;align-items:baseline;
  font-family:'Plex Mono',monospace;font-size:6.6pt;letter-spacing:.18em;
  text-transform:uppercase;color:var(--grafite);
}}
.page.escura .cab{{color:var(--nevoa-fria)}}
.regua{{position:absolute;left:var(--m);right:var(--m);top:calc(var(--m) + 5.2mm);height:.4pt;background:var(--nevoa)}}
.page.escura .regua{{background:#265046}}
.rod{{
  position:absolute;bottom:var(--m);left:var(--m);right:var(--m);
  display:flex;justify-content:space-between;align-items:baseline;
  font-family:'Plex Mono',monospace;font-size:6.6pt;color:var(--grafite);letter-spacing:.1em;
}}
.page.escura .rod{{color:var(--nevoa-fria)}}
.corpo{{position:absolute;left:var(--m);right:var(--m);top:calc(var(--m) + 13mm);bottom:calc(var(--m) + 8mm)}}

/* --- tipografia --- */
.h1{{font-family:'Outfit',sans-serif;font-weight:700;font-size:26pt;line-height:1.12;letter-spacing:-.015em}}
.h2{{font-family:'Outfit',sans-serif;font-weight:700;font-size:15pt;line-height:1.2;letter-spacing:-.01em}}
.olho{{font-family:'Plex Mono',monospace;font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--folha);margin-bottom:3.5mm}}
.txt{{font-size:9.6pt;line-height:1.62;color:var(--grafite);max-width:78mm}}
.txt strong{{color:var(--tinta);font-weight:700}}
.leg{{font-family:'Plex Mono',monospace;font-size:6.6pt;letter-spacing:.1em;color:var(--grafite);text-transform:uppercase}}
.dado{{font-family:'Plex Mono',monospace;font-size:7.6pt;color:var(--tinta)}}

/* --- assinatura --- */
.lockup{{display:flex}}
.lk-h{{flex-direction:row;align-items:center;gap:3.2mm}}
.lk-v{{flex-direction:column;align-items:center;gap:2.6mm}}
.lk-nome{{font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:.02em;line-height:1}}
.lk-desc{{font-size:6.6pt;letter-spacing:.04em;opacity:.72;margin-top:1.2mm;max-width:62mm}}
.lk-desc-c{{text-align:center}}

/* --- capa --- */
.capa-marca{{position:absolute;left:var(--m);top:50%;transform:translateY(-56%)}}
.capa-nome{{font-family:'Outfit',sans-serif;font-weight:700;font-size:64pt;color:var(--papel);letter-spacing:.01em;line-height:.94;margin-top:7mm}}
.capa-desc{{font-size:11pt;color:var(--descritor);margin-top:4mm;max-width:96mm;line-height:1.5}}
.capa-pe{{position:absolute;left:var(--m);bottom:var(--m);font-family:'Plex Mono',monospace;font-size:7pt;letter-spacing:.14em;color:var(--nevoa-fria);text-transform:uppercase;line-height:1.9}}
.capa-aneis{{position:absolute;right:-58mm;top:50%;transform:translateY(-50%);opacity:.16}}

/* --- grades --- */
.cols{{display:flex;gap:12mm;height:100%}}
.col-txt{{width:80mm;flex:none}}
.col-viz{{flex:1;position:relative}}
.centro{{display:flex;align-items:center;justify-content:center;height:100%}}

/* --- cor --- */
.swatches{{display:flex;gap:4mm}}
.sw{{flex:1}}
.sw-chip{{height:34mm;border-radius:1.6mm;border:.4pt solid rgba(16,26,23,.10)}}
.sw-nome{{font-family:'Outfit',sans-serif;font-weight:700;font-size:10pt;margin-top:2.6mm}}
.sw-hex{{font-family:'Plex Mono',monospace;font-size:7.4pt;color:var(--tinta);margin-top:.8mm}}
.sw-rgb{{font-family:'Plex Mono',monospace;font-size:6.6pt;color:var(--grafite);margin-top:.4mm}}
.sw-papel{{font-size:7.4pt;line-height:1.45;color:var(--grafite);margin-top:1.8mm}}

/* --- status --- */
.status-linha{{display:flex;align-items:center;gap:4mm;padding:4.6mm 0;border-bottom:.4pt solid var(--nevoa)}}
.status-linha:last-child{{border-bottom:none}}
.pill{{
  display:inline-flex;align-items:center;gap:1.6mm;
  padding:1.3mm 3.2mm;border-radius:9mm;color:#fff;
  font-size:7.4pt;font-weight:700;letter-spacing:.02em;white-space:nowrap;
}}
.pill i{{width:1.7mm;height:1.7mm;border-radius:50%;background:rgba(255,255,255,.9);display:block}}
.status-prazo{{font-family:'Plex Mono',monospace;font-size:7.4pt;color:var(--tinta);width:38mm;flex:none}}
.status-papel{{font-size:8pt;color:var(--grafite);line-height:1.4}}
.status-hex{{font-family:'Plex Mono',monospace;font-size:6.8pt;color:var(--grafite);margin-left:auto}}

/* --- tabela --- */
table{{width:100%;border-collapse:collapse}}
th{{
  font-family:'Plex Mono',monospace;font-size:6.4pt;letter-spacing:.16em;text-transform:uppercase;
  color:var(--grafite);text-align:left;padding-bottom:2.2mm;border-bottom:.5pt solid var(--nevoa);font-weight:400;
}}
td{{padding:2.5mm 0;border-bottom:.4pt solid var(--nevoa);font-size:8.4pt;vertical-align:baseline}}
td.mono{{font-family:'Plex Mono',monospace;font-size:7.6pt;color:var(--grafite);white-space:nowrap}}

/* --- caixas --- */
.tile{{background:var(--branco);border:.4pt solid var(--nevoa);border-radius:2mm;position:relative;overflow:hidden}}
.grade4{{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}}
.mau{{aspect-ratio:1.32;display:flex;align-items:center;justify-content:center;position:relative}}
.mau-cap{{position:absolute;left:0;right:0;bottom:0;padding:2.2mm 3mm;font-size:7pt;color:var(--grafite);border-top:.4pt solid var(--nevoa);background:var(--papel)}}
.mau-x{{position:absolute;top:2.4mm;right:2.6mm;width:4.4mm;height:4.4mm;border-radius:50%;background:var(--critico);color:#fff;font-size:7pt;font-weight:700;display:flex;align-items:center;justify-content:center;line-height:1}}

/* --- ícone --- */
.icone{{border-radius:22.4%;display:flex;align-items:center;justify-content:center;overflow:hidden}}

/* --- interface --- */
.tela{{width:62mm;border-radius:4mm;overflow:hidden;border:.5pt solid var(--nevoa);background:var(--branco)}}
.tela-topo{{background:var(--verde);padding:5mm 4.5mm 4mm}}
.tela-tit{{font-family:'Outfit',sans-serif;font-weight:700;font-size:11pt;color:#fff}}
.tela-sub{{font-size:6.8pt;color:var(--descritor);margin-top:.8mm;font-family:'Plex Mono',monospace;letter-spacing:.08em}}
.card{{padding:3.4mm 4.5mm;border-bottom:.4pt solid var(--nevoa)}}
.card-topo{{display:flex;justify-content:space-between;align-items:center;gap:2mm}}
.card-nome{{font-size:8pt;font-weight:700;color:var(--tinta)}}
.card-meta{{font-family:'Plex Mono',monospace;font-size:6.2pt;color:var(--grafite);margin-top:1.1mm;letter-spacing:.04em}}
.barra{{height:1.5mm;border-radius:1mm;background:var(--nevoa);margin-top:2.4mm;overflow:hidden}}
.barra i{{display:block;height:100%;border-radius:1mm}}
"""


# ----------------------------------------------------------------- as páginas

def moldura(tokens, n, total, secao, conteudo, escura=False):
    cls = "page escura" if escura else "page"
    return f"""
<section class="{cls}">
  <div class="cab"><span>{secao}</span><span>BIOSS · Identidade Visual · v{tokens["marca"]["versao"]}</span></div>
  <div class="regua"></div>
  <div class="corpo">{conteudo}</div>
  <div class="rod"><span>Biogênese Licenciamento Ambiental</span><span>{n:02d} / {total:02d}</span></div>
</section>"""


def p_capa(tokens):
    aneis = "".join(
        f'<circle cx="300" cy="300" r="{r}" fill="none" stroke="#F7F9F6" stroke-width="1.1"/>'
        for r in range(46, 300, 26)
    )
    return f"""
<section class="page escura">
  <div class="capa-aneis">
    <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">{aneis}</svg>
  </div>
  <div class="capa-marca">
    {simbolo(tokens, "#2F9E6B", 108)}
    <div class="capa-nome">BIOSS</div>
    <div class="capa-desc">{tokens["marca"]["descritor"]}</div>
  </div>
  <div class="capa-pe">
    Manual de Identidade Visual · Versão {tokens["marca"]["versao"]}<br>
    {tokens["marca"]["organizacao"]} · Caxias do Sul / RS
  </div>
</section>"""


def p_conceito(tokens):
    s = tokens["simbolo"]
    conteudo = f"""
<div class="cols">
  <div class="col-txt">
    <div class="olho">01 · Conceito</div>
    <div class="h1">Anel de<br>Crescimento</div>
    <div class="txt" style="margin-top:6mm">
      O licenciamento ambiental corre em dois relógios. Um é biológico — estações,
      ciclos, o tempo próprio do ecossistema. O outro é regulatório — vigências,
      condicionantes, prazos que não se movem.
    </div>
    <div class="txt" style="margin-top:3.6mm">
      O anel de crescimento é o ponto em que os dois coincidem: <strong>uma marca do tempo
      que se lê como círculo</strong>. Registra o que passou e mostra o que falta.
    </div>
    <div class="txt" style="margin-top:3.6mm">
      No símbolo, o anel externo permanece <strong>aberto</strong>. É o prazo em curso —
      fecha quando o ciclo se cumpre.
    </div>
  </div>
  <div class="col-viz">
    <div class="centro">{simbolo(tokens, "#0E3B32", 300)}</div>
    <div style="position:absolute;left:0;bottom:0;right:0;display:flex;gap:8mm">
      <div style="flex:1"><div class="leg">Leitura A</div>
        <div class="txt" style="font-size:8.4pt;margin-top:1.4mm">Anel de árvore — matéria viva, tempo acumulado.</div></div>
      <div style="flex:1"><div class="leg">Leitura B</div>
        <div class="txt" style="font-size:8.4pt;margin-top:1.4mm">Anel de progresso — prazo em curso, ciclo por fechar.</div></div>
      <div style="flex:1"><div class="leg">Excentricidade</div>
        <div class="txt" style="font-size:8.4pt;margin-top:1.4mm">{s["excentricidade_curta"]}, como no crescimento real.</div></div>
    </div>
  </div>
</div>"""
    return moldura(tokens, 2, 13, "Conceito", conteudo)


def p_construcao(tokens):
    s = tokens["simbolo"]
    g = s["grid"]
    guias = "".join(
        f'<line x1="{i}" y1="0" x2="{i}" y2="{g}" stroke="#D8E0DA" stroke-width=".4"/>'
        f'<line x1="0" y1="{i}" x2="{g}" y2="{i}" stroke="#D8E0DA" stroke-width=".4"/>'
        for i in range(0, g + 1, 10)
    )
    eixos = (
        f'<line x1="60" y1="0" x2="60" y2="{g}" stroke="#A9BCB1" stroke-width=".7"/>'
        f'<line x1="0" y1="60" x2="{g}" y2="60" stroke="#A9BCB1" stroke-width=".7"/>'
    )
    # No símbolo, só a cruzeta do centro geométrico — os quatro centros ficam a
    # 4,5 unidades entre si e viram um borrão nesta escala. Vão no detalhe ampliado.
    marcas = (
        '<line x1="54" y1="60" x2="66" y2="60" stroke="#C0492F" stroke-width=".9"/>'
        '<line x1="60" y1="54" x2="60" y2="66" stroke="#C0492F" stroke-width=".9"/>'
    )

    # Detalhe ×8 dos centros deslocados.
    amp = 8
    base = s["aneis"][0]["centro"]
    pts = [((a["centro"][0] - base[0]) * amp + 46, (a["centro"][1] - base[1]) * amp + 46)
           for a in s["aneis"]]
    detalhe = (
        f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[-1][0]}" y2="{pts[-1][1]}" '
        f'stroke="#C0492F" stroke-width=".8" stroke-dasharray="2 2"/>'
        + "".join(
            f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke="#C0492F" stroke-width="1.2"/>'
            f'<circle cx="{x}" cy="{y}" r=".9" fill="#C0492F"/>'
            for x, y in pts
        )
    )
    corpo_svg = simbolo(tokens, "#0E3B32", 300).replace(
        "<svg", '<svg style="position:absolute;inset:0"', 1
    )

    def celula_arco(a):
        if a.get("preenchido"):
            return "—"
        if a.get("aberto"):
            return f'aberto {a["gap_inicio"]}°–{a["gap_fim"]}°'
        return "fechado"

    linhas = "".join(
        f"""<tr><td>{a["nome"]}</td>
        <td class="mono">{a["raio"]}</td>
        <td class="mono">{a["centro"][0]} , {a["centro"][1]}</td>
        <td class="mono">{"sólido" if a.get("preenchido") else a["traco"]}</td>
        <td class="mono">{celula_arco(a)}</td></tr>"""
        for a in s["aneis"]
    )

    conteudo = f"""
<div class="cols">
  <div class="col-txt">
    <div class="olho">02 · Símbolo</div>
    <div class="h1">Construção</div>
    <div class="txt" style="margin-top:5mm">
      O símbolo é desenhado sobre grade de <strong>{g} × {g}</strong>. Todos os raios e
      deslocamentos derivam dela — nunca redesenhe à mão.
    </div>
    <table style="margin-top:6mm">
      <colgroup><col style="width:18%"><col style="width:10%"><col style="width:29%"><col style="width:15%"><col></colgroup>
      <tr><th>Anel</th><th>Raio</th><th>Centro</th><th>Traço</th><th>Arco</th></tr>
      {linhas}
    </table>
    <div class="txt" style="font-size:8pt;margin-top:5mm">
      A abertura do anel externo vai de <strong>{s["aneis"][0]["gap_inicio"]}°</strong> a
      <strong>{s["aneis"][0]["gap_fim"]}°</strong>, medidos no sentido horário a partir das 12 horas.
    </div>
  </div>
  <div class="col-viz">
    <div class="centro">
      <div style="position:relative;width:300px;height:300px">
        <svg style="position:absolute;inset:0" width="300" height="300" viewBox="0 0 {g} {g}" xmlns="http://www.w3.org/2000/svg">
          {guias}{eixos}
        </svg>
        {corpo_svg}
        <svg style="position:absolute;inset:0" width="300" height="300" viewBox="0 0 {g} {g}" xmlns="http://www.w3.org/2000/svg">
          {marcas}
        </svg>
      </div>
    </div>
    <div style="position:absolute;left:0;bottom:0;display:flex;align-items:flex-end;gap:6mm">
      <div class="tile" style="padding:3mm 3mm 2mm">
        <svg style="display:block;margin:0 auto" width="76" height="76" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg">{detalhe}</svg>
        <div class="leg" style="margin-top:1mm">Detalhe ×{amp} · os quatro centros</div>
      </div>
      <div class="txt" style="font-size:8.4pt;max-width:74mm;padding-bottom:1mm">
        Do anel externo ao núcleo, o centro caminha <strong>4,5 unidades</strong> rumo ao
        quadrante superior esquerdo. A cruzeta vermelha no símbolo marca o centro geométrico
        da grade — nenhum anel está sobre ele, exceto o externo.
      </div>
    </div>
  </div>
</div>"""
    return moldura(tokens, 3, 13, "Símbolo · Construção", conteudo)


def p_assinaturas(tokens):
    conteudo = f"""
<div class="olho">03 · Assinaturas</div>
<div class="h1" style="margin-bottom:7mm">Versões oficiais</div>
<div style="display:flex;gap:5mm;height:74mm">
  <div class="tile" style="flex:1.5;display:flex;align-items:center;justify-content:center">
    {logotipo(tokens, "#0E3B32", 40, "horizontal", True)}
  </div>
  <div class="tile" style="flex:1;display:flex;align-items:center;justify-content:center">
    {logotipo(tokens, "#0E3B32", 42, "vertical", True)}
  </div>
  <div class="tile" style="flex:.62;display:flex;align-items:center;justify-content:center">
    {simbolo(tokens, "#0E3B32", 86)}
  </div>
</div>
<div style="display:flex;gap:5mm;margin-top:4mm;height:44mm">
  <div style="flex:1.5;background:var(--verde);border-radius:2mm;display:flex;align-items:center;justify-content:center">
    {logotipo(tokens, "#F7F9F6", 30, "horizontal")}
  </div>
  <div style="flex:1;background:var(--verde);border-radius:2mm;display:flex;align-items:center;justify-content:center">
    {logotipo(tokens, "#2F9E6B", 30, "horizontal")}
  </div>
  <div style="flex:.62;background:var(--tinta);border-radius:2mm;display:flex;align-items:center;justify-content:center">
    {simbolo(tokens, "#F7F9F6", 54)}
  </div>
</div>
<div style="display:flex;gap:5mm;margin-top:2.6mm">
  <div style="flex:1.5"><div class="leg">Horizontal · preferencial</div></div>
  <div style="flex:1"><div class="leg">Vertical · espaços estreitos</div></div>
  <div style="flex:.62"><div class="leg">Símbolo · app e favicon</div></div>
</div>"""
    return moldura(tokens, 4, 13, "Assinaturas", conteudo)


def p_protecao(tokens):
    s = tokens["simbolo"]
    lado = 150                                   # tamanho do símbolo no diagrama
    nucleo = next(a for a in s["aneis"] if a.get("preenchido"))
    x = 2 * nucleo["raio"] / s["grid"] * lado     # X = diâmetro do núcleo, na escala exibida
    conteudo = f"""
<div class="cols">
  <div class="col-txt">
    <div class="olho">04 · Aplicação</div>
    <div class="h1">Respiro e<br>reduções</div>
    <div class="txt" style="margin-top:5mm">
      A área de proteção equivale a <strong>X</strong>, o diâmetro do núcleo do símbolo —
      <strong>{2 * nucleo["raio"]:.0f}</strong> unidades da grade. Nenhum texto, imagem ou
      borda entra nessa faixa.
    </div>
    <table style="margin-top:6mm">
      <colgroup><col style="width:42%"><col style="width:26%"><col></colgroup>
      <tr><th>Suporte</th><th>Mínimo</th><th>Versão</th></tr>
      <tr><td>Tela</td><td class="mono">{s["reducao_minima_digital"]}</td><td class="mono">completa</td></tr>
      <tr><td>Tela · favicon</td><td class="mono">16 px</td><td class="mono">simplificada</td></tr>
      <tr><td>Impresso</td><td class="mono">{s["reducao_minima_impressa"]}</td><td class="mono">completa</td></tr>
    </table>
    <div class="txt" style="font-size:8pt;margin-top:5mm">
      Abaixo de 24 px o anel médio e o interno se fecham visualmente. Use a
      <strong>versão simplificada</strong>: anel externo e núcleo apenas.
    </div>
  </div>
  <div class="col-viz">
    <div style="display:flex;align-items:center;justify-content:center;height:64%">
      <div style="position:relative;padding:{x:.1f}px">
        <div style="position:absolute;inset:0;border:.8pt dashed #A9BCB1;border-radius:2mm"></div>
        <!-- cota de X: traço com serifas nas pontas e rótulo acima, sem tocar o traço -->
        <div style="position:absolute;left:0;top:50%;width:{x:.1f}px;height:.7pt;background:#C0492F"></div>
        <div style="position:absolute;left:0;top:calc(50% - 2.4px);width:.7pt;height:5.5px;background:#C0492F"></div>
        <div style="position:absolute;left:{x - 0.7:.1f}px;top:calc(50% - 2.4px);width:.7pt;height:5.5px;background:#C0492F"></div>
        <div style="position:absolute;left:0;width:{x:.1f}px;top:calc(50% - 15px);text-align:center;
                    font-family:'Plex Mono';font-size:6.4pt;color:#C0492F">X</div>
        {simbolo(tokens, "#0E3B32", lado)}
      </div>
    </div>
    <div style="display:flex;gap:9mm;align-items:flex-end;justify-content:center;margin-top:4mm">
      <div style="text-align:center">{simbolo(tokens, "#0E3B32", 64)}<div class="leg" style="margin-top:2mm">64 px</div></div>
      <div style="text-align:center">{simbolo(tokens, "#0E3B32", 32)}<div class="leg" style="margin-top:2mm">32 px</div></div>
      <div style="text-align:center">{simbolo(tokens, "#0E3B32", 24)}<div class="leg" style="margin-top:2mm">24 px</div></div>
      <div style="text-align:center">{simbolo(tokens, "#0E3B32", 16, simplificado=True)}<div class="leg" style="margin-top:2mm">16 px · simpl.</div></div>
    </div>
  </div>
</div>"""
    return moldura(tokens, 5, 13, "Respiro e Reduções", conteudo)


def p_indevidos(tokens):
    sym = lambda cor="#0E3B32", t=54: simbolo(tokens, cor, t)
    casos = [
        ("Não distorça as proporções.", f'<div style="transform:scaleX(1.42)">{sym()}</div>'),
        ("Não gire o símbolo.", f'<div style="transform:rotate(28deg)">{sym()}</div>'),
        ("Não recolora fora da paleta.", sym("#7B4DB8")),
        ("Não aplique contorno ou sombra.",
         f'<div style="filter:drop-shadow(2.4px 3px 2px rgba(0,0,0,.45))">{sym()}</div>'),
        ("Não use sobre fundo de baixo contraste.",
         f'<div style="background:#2F9E6B;padding:5mm;border-radius:2mm">{sym("#3FAE7B")}</div>'),
        ("Não altere a abertura do anel.",
         f'<svg width="54" height="54" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">'
         f'<circle cx="60" cy="60" r="52" fill="none" stroke="#0E3B32" stroke-width="7"/>'
         f'<circle cx="58.5" cy="58.5" r="39" fill="none" stroke="#0E3B32" stroke-width="6"/>'
         f'<circle cx="57" cy="57" r="26.5" fill="none" stroke="#0E3B32" stroke-width="5"/>'
         f'<circle cx="55.5" cy="55.5" r="9.5" fill="#0E3B32"/></svg>'),
    ]
    tiles = "".join(
        f"""<div class="tile mau"><div class="mau-x">×</div>{viz}<div class="mau-cap">{txt}</div></div>"""
        for txt, viz in casos
    )
    conteudo = f"""
<div class="olho">05 · Aplicação</div>
<div class="h1" style="margin-bottom:6mm">Usos indevidos</div>
<div class="grade4">{tiles}</div>"""
    return moldura(tokens, 6, 13, "Usos Indevidos", conteudo)


def p_cor_institucional(tokens):
    inst = tokens["cor"]["institucional"]
    neut = tokens["cor"]["neutro"]

    def chip(c, altura="34mm"):
        r, g, b = rgb(c["hex"])
        return f"""
        <div class="sw">
          <div class="sw-chip" style="background:{c["hex"]};height:{altura}"></div>
          <div class="sw-nome">{c["nome"]}</div>
          <div class="sw-hex">{c["hex"].upper()}</div>
          <div class="sw-rgb">RGB {r} {g} {b}</div>
          <div class="sw-papel">{c["papel"]}</div>
        </div>"""

    def por_id(grupo, ident):
        return next(c for c in tokens["cor"][grupo] if c["id"] == ident)["hex"]

    verde, papel = por_id("institucional", "verde-profundo"), por_id("neutro", "papel")
    branco, folha = por_id("neutro", "branco"), por_id("institucional", "verde-folha")

    def nota(frente, fundo, rotulo):
        v = contraste(frente, fundo)
        return (f'<div class="dado">{rotulo} · contraste {v:.1f}:1 · '
                f'{"AAA" if v >= 7 else "AA"}</div>')

    conteudo = f"""
<div class="olho">06 · Cor</div>
<div class="h1" style="margin-bottom:6mm">Paleta institucional</div>
<div class="swatches">{"".join(chip(c) for c in inst)}</div>
<div style="height:6mm"></div>
<div class="leg" style="margin-bottom:2.6mm">Neutros</div>
<div class="swatches">{"".join(chip(c, "17mm") for c in neut)}</div>
<div style="position:absolute;bottom:0;left:0;right:0;display:flex;gap:9mm;border-top:.4pt solid var(--nevoa);padding-top:3mm">
  {nota(verde, papel, "Verde Profundo sobre Papel")}
  {nota(papel, verde, "Papel sobre Verde Profundo")}
  {nota(branco, folha, "Branco sobre Verde Folha")}
</div>"""
    return moldura(tokens, 7, 13, "Cor Institucional", conteudo)


def p_cor_funcional(tokens):
    fn = tokens["cor"]["funcional"]
    linhas = "".join(
        f"""<div class="status-linha">
          <span class="pill" style="background:{c["hex"]}"><i></i>{c["nome"]}</span>
          <span class="status-prazo">{c["prazo"]}</span>
          <span class="status-papel">{c["papel"]}</span>
          <span class="status-hex">{c["hex"].upper()}</span>
        </div>"""
        for c in fn
    )
    conteudo = f"""
<div class="cols">
  <div class="col-txt">
    <div class="olho">07 · Cor</div>
    <div class="h1">Sistema<br>de estado</div>
    <div class="txt" style="margin-top:5mm">
      O BIOSS existe para responder a uma pergunta: <strong>o que vence primeiro?</strong>
      A cor responde antes da leitura.
    </div>
    <div class="txt" style="margin-top:3.6mm">
      Cinco estados, nunca mais. Cada um vale para licença, condicionante e protocolo —
      a mesma cor significa a mesma coisa em toda a interface.
    </div>
    <div class="txt" style="font-size:8pt;margin-top:5mm;border-left:1.4pt solid var(--nevoa);padding-left:3.4mm">
      A cor nunca é o único sinal. Todo estado carrega também rótulo em texto,
      para leitores com baixa visão cromática.
    </div>
  </div>
  <div class="col-viz">
    <div style="height:100%;display:flex;flex-direction:column;justify-content:center">{linhas}</div>
  </div>
</div>"""
    return moldura(tokens, 8, 13, "Cor Funcional", conteudo)


def p_tipografia(tokens):
    t = tokens["tipografia"]
    escala = "".join(
        f"""<tr><td>{e["nome"]}</td><td class="mono">{e["tamanho"]}</td>
        <td class="mono">{e["entrelinha"]}</td><td class="mono">{e["peso"]}</td>
        <td style="color:var(--grafite);font-size:8pt">{e["uso"]}</td></tr>"""
        for e in t["escala"]
    )
    conteudo = f"""
<div class="olho">08 · Tipografia</div>
<div class="h1" style="margin-bottom:6mm">Três vozes</div>
<div style="display:flex;gap:6mm;margin-bottom:6mm">
  <div class="tile" style="flex:1;padding:5mm">
    <div class="leg">Display · {t["display"]["familia"]}</div>
    <div style="font-family:'Outfit';font-weight:700;font-size:32pt;margin-top:2.4mm;letter-spacing:-.02em">Aa</div>
    <div style="font-family:'Outfit';font-size:9pt;color:var(--grafite);margin-top:1mm">ABCDEFGHIJ · 0123456789</div>
    <div class="sw-papel" style="margin-top:2.6mm">{t["display"]["papel"]}</div>
  </div>
  <div class="tile" style="flex:1;padding:5mm">
    <div class="leg">Texto · {t["texto"]["familia"]}</div>
    <div style="font-family:'Work Sans';font-weight:700;font-size:32pt;margin-top:2.4mm">Aa</div>
    <div style="font-family:'Work Sans';font-size:9pt;color:var(--grafite);margin-top:1mm">ABCDEFGHIJ · 0123456789</div>
    <div class="sw-papel" style="margin-top:2.6mm">{t["texto"]["papel"]}</div>
  </div>
  <div class="tile" style="flex:1;padding:5mm">
    <div class="leg">Dados · {t["dados"]["familia"]}</div>
    <div style="font-family:'Plex Mono';font-weight:700;font-size:32pt;margin-top:2.4mm">Aa</div>
    <div style="font-family:'Plex Mono';font-size:8.4pt;color:var(--grafite);margin-top:1mm">LP 013/2023 · 30.677</div>
    <div class="sw-papel" style="margin-top:2.6mm">{t["dados"]["papel"]}</div>
  </div>
</div>
<table>
  <tr><th>Nível</th><th>Corpo</th><th>Entrelinha</th><th>Peso</th><th>Uso</th></tr>
  {escala}
</table>"""
    return moldura(tokens, 9, 13, "Tipografia", conteudo)


def p_icone(tokens):
    g = tokens["simbolo"]["grid"]
    conteudo = f"""
<div class="cols">
  <div class="col-txt">
    <div class="olho">09 · Produto</div>
    <div class="h1">Ícone do<br>aplicativo</div>
    <div class="txt" style="margin-top:5mm">
      O símbolo ocupa <strong>68%</strong> da largura do ícone, centrado na área segura.
      Fundo em Verde Profundo, símbolo em Verde Vivo.
    </div>
    <table style="margin-top:6mm">
      <colgroup><col style="width:30%"><col style="width:24%"><col></colgroup>
      <tr><th>Plataforma</th><th>Base</th><th>Raio</th></tr>
      <tr><td>iOS</td><td class="mono">1024 px</td><td class="mono">squircle 22,4%</td></tr>
      <tr><td>Android</td><td class="mono">432 px</td><td class="mono">adaptativo · 66 px seguros</td></tr>
      <tr><td>Web</td><td class="mono">512 px</td><td class="mono">maskable</td></tr>
    </table>
  </div>
  <div class="col-viz">
    <div style="display:flex;align-items:center;justify-content:center;gap:8mm;height:66%">
      <div style="position:relative">
        <div class="icone" style="width:150px;height:150px;background:var(--verde)">
          {simbolo(tokens, "#2F9E6B", 102)}
        </div>
        <div style="position:absolute;inset:13px;border:.6pt dashed rgba(247,249,246,.45);border-radius:50%"></div>
      </div>
      <div class="icone" style="width:150px;height:150px;background:var(--papel);border:.4pt solid var(--nevoa)">
        {simbolo(tokens, "#0E3B32", 102)}
      </div>
    </div>
    <div style="display:flex;gap:6mm;align-items:flex-end;justify-content:center">
      <div style="text-align:center"><div class="icone" style="width:60px;height:60px;background:var(--verde)">{simbolo(tokens, "#2F9E6B", 41)}</div><div class="leg" style="margin-top:2mm">120</div></div>
      <div style="text-align:center"><div class="icone" style="width:40px;height:40px;background:var(--verde)">{simbolo(tokens, "#2F9E6B", 27)}</div><div class="leg" style="margin-top:2mm">80</div></div>
      <div style="text-align:center"><div class="icone" style="width:29px;height:29px;background:var(--verde)">{simbolo(tokens, "#2F9E6B", 20, simplificado=True)}</div><div class="leg" style="margin-top:2mm">58</div></div>
    </div>
    <div style="position:absolute;bottom:0;left:0"><div class="leg">Área segura tracejada · grade {g}</div></div>
  </div>
</div>"""
    return moldura(tokens, 10, 13, "Ícone do Aplicativo", conteudo)


def p_interface(tokens):
    fn = {c["id"]: c for c in tokens["cor"]["funcional"]}

    def card(nome, meta, estado, pct):
        c = fn[estado]
        return f"""
        <div class="card">
          <div class="card-topo">
            <span class="card-nome">{nome}</span>
            <span class="pill" style="background:{c["hex"]};font-size:6pt;padding:1mm 2.4mm"><i style="width:1.3mm;height:1.3mm"></i>{c["nome"]}</span>
          </div>
          <div class="card-meta">{meta}</div>
          <div class="barra"><i style="width:{pct}%;background:{c["hex"]}"></i></div>
        </div>"""

    conteudo = f"""
<div class="cols">
  <div class="col-txt">
    <div class="olho">10 · Produto</div>
    <div class="h1">Interface</div>
    <div class="txt" style="margin-top:5mm">
      O anel reaparece como <strong>barra de prazo</strong>: a mesma ideia de ciclo
      por fechar, esticada na horizontal.
    </div>
    <div class="txt" style="margin-top:3.6mm">
      Cartões em Branco sobre Papel. Cabeçalho em Verde Profundo.
      Números de protocolo sempre em Plex Mono — alinham em coluna e não confundem 0 com O.
    </div>
    <div style="margin-top:6mm">
      <div class="leg" style="margin-bottom:2.4mm">Etiquetas de estado</div>
      <div style="display:flex;flex-wrap:wrap;gap:2.2mm">
        {"".join(f'<span class="pill" style="background:{c["hex"]}"><i></i>{c["nome"]}</span>' for c in tokens["cor"]["funcional"])}
      </div>
    </div>
  </div>
  <div class="col-viz">
    <div style="height:100%;display:flex;gap:6mm;justify-content:center;align-items:center">
      <div class="tela">
        <div class="tela-topo">
          <div class="tela-tit">Prazos</div>
          <div class="tela-sub">14 ATIVOS · 3 CRÍTICOS</div>
        </div>
        {card("Licença de Operação", "LO 4471/2024 · vence 12/09/2026", "critico", 88)}
        {card("Renovação · Outorga", "PROC 0.025590/2023-88 · 47 dias", "atencao", 61)}
        {card("Condicionante 07", "Monitoramento trimestral · 118 dias", "regular", 24)}
        {card("Licença Prévia", "LP 013/2023 · expirada 30/06/2026", "vencido", 100)}
      </div>
      <div class="tela" style="width:52mm">
        <div class="tela-topo" style="background:var(--papel);border-bottom:.4pt solid var(--nevoa)">
          <div class="tela-tit" style="color:var(--tinta)">Empreendimento</div>
          <div class="tela-sub" style="color:var(--grafite)">CNPJ 21.835.729/0001-58</div>
        </div>
        <div style="padding:4.5mm">
          <div class="leg">Situação geral</div>
          <div style="display:flex;align-items:center;gap:3mm;margin-top:3mm">
            {simbolo(tokens, tokens["cor"]["funcional"][1]["hex"], 46)}
            <div>
              <div style="font-family:'Outfit';font-weight:700;font-size:15pt;color:var(--atencao)">61%</div>
              <div class="card-meta" style="margin-top:0">do ciclo decorrido</div>
            </div>
          </div>
          <div style="height:4mm"></div>
          <div class="leg">Próximo vencimento</div>
          <div class="dado" style="margin-top:1.6mm">12 / 09 / 2026</div>
        </div>
      </div>
    </div>
  </div>
</div>"""
    return moldura(tokens, 11, 13, "Interface", conteudo)


def p_aplicacoes(tokens):
    conteudo = f"""
<div class="olho">11 · Aplicações</div>
<div class="h1" style="margin-bottom:6mm">No mundo</div>
<div style="display:flex;gap:5mm;height:96mm">
  <div style="flex:.8;background:var(--verde);border-radius:3mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4mm">
    {simbolo(tokens, "#2F9E6B", 66)}
    <div style="font-family:'Outfit';font-weight:700;font-size:20pt;color:#F7F9F6;letter-spacing:.02em">BIOSS</div>
    <div style="position:absolute"></div>
  </div>
  <div class="tile" style="flex:1.35;padding:6mm;display:flex;flex-direction:column;justify-content:center">
    <div class="leg" style="margin-bottom:4mm">Assinatura de e-mail</div>
    <div style="display:flex;gap:4mm;align-items:center">
      <div style="width:.8pt;background:var(--folha);align-self:stretch"></div>
      <div>
        <div style="font-family:'Outfit';font-weight:700;font-size:11pt">Cleber Jr. de Souza Saraiva</div>
        <div style="font-size:8pt;color:var(--grafite);margin-top:.6mm">Biólogo · CRBio 88707/03-D</div>
        <div style="height:2.6mm"></div>
        {logotipo(tokens, "#0E3B32", 22, "horizontal")}
        <div class="dado" style="margin-top:2.4mm;font-size:6.8pt;color:var(--grafite)">
          biogeneseambiental.com · Caxias do Sul / RS
        </div>
      </div>
    </div>
  </div>
  <div class="tile" style="flex:1;padding:0;overflow:hidden;display:flex;flex-direction:column">
    <div style="background:var(--verde);padding:5mm;display:flex;justify-content:space-between;align-items:center">
      {logotipo(tokens, "#F7F9F6", 20, "horizontal")}
      <span class="leg" style="color:var(--nevoa-fria)">Relatório</span>
    </div>
    <div style="padding:5mm;flex:1">
      <div style="font-family:'Outfit';font-weight:700;font-size:12pt;line-height:1.2">Relatório mensal<br>de conformidade</div>
      <div class="dado" style="margin-top:3mm;color:var(--grafite)">AGO / 2026</div>
      <div style="margin-top:5mm">
        {"".join(f'<div style="height:1.1mm;background:var(--nevoa);border-radius:1mm;margin-bottom:2mm;width:{w}%"></div>' for w in [100, 86, 94, 62])}
      </div>
      <div style="display:flex;gap:2mm;margin-top:4mm">
        <span class="pill" style="background:var(--regular);font-size:6pt;padding:.9mm 2.2mm"><i style="width:1.2mm;height:1.2mm"></i>Em dia</span>
        <span class="pill" style="background:var(--atencao);font-size:6pt;padding:.9mm 2.2mm"><i style="width:1.2mm;height:1.2mm"></i>Atenção</span>
      </div>
    </div>
  </div>
</div>
<div style="display:flex;gap:5mm;margin-top:2.6mm">
  <div style="flex:.8"><div class="leg">Splash</div></div>
  <div style="flex:1.35"><div class="leg">Assinatura</div></div>
  <div style="flex:1"><div class="leg">Documento</div></div>
</div>"""
    return moldura(tokens, 12, 13, "Aplicações", conteudo)


def p_colofao(tokens):
    t = tokens["tipografia"]
    conteudo = f"""
<div class="cols">
  <div class="col-txt">
    <div class="olho">12 · Colofão</div>
    <div class="h1">Sobre este<br>manual</div>
    <div class="txt" style="margin-top:5mm">
      Documento gerado por <strong>build.py</strong> a partir de <strong>tokens.json</strong>.
      Toda cor, medida e escala vem daquele arquivo — altere lá e reconstrua,
      nunca edite o PDF.
    </div>
    <div class="dado" style="margin-top:6mm;line-height:2">
      python3 build.py
    </div>
  </div>
  <div class="col-viz">
    <div class="leg" style="margin-bottom:2.6mm">Tipos e licenças</div>
    <table>
      <tr><th>Família</th><th>Papel</th><th>Licença</th></tr>
      <tr><td>{t["display"]["familia"]}</td><td style="color:var(--grafite);font-size:8pt">Display</td><td class="mono">OFL 1.1</td></tr>
      <tr><td>{t["texto"]["familia"]}</td><td style="color:var(--grafite);font-size:8pt">Texto e interface</td><td class="mono">OFL 1.1</td></tr>
      <tr><td>{t["dados"]["familia"]}</td><td style="color:var(--grafite);font-size:8pt">Dados técnicos</td><td class="mono">OFL 1.1</td></tr>
    </table>
    <div style="height:7mm"></div>
    <div class="leg" style="margin-bottom:2.6mm">Aberto nesta versão</div>
    <div class="txt" style="font-size:8.4pt;max-width:none">
      Os limiares de prazo do sistema de estado (60 / 30 dias) são proposta —
      confirmar com a operação. A expansão da sigla BIOSS permanece em aberto:
      o manual trata o nome como palavra, não como acrônimo.
    </div>
    <div style="position:absolute;bottom:0;right:0">{simbolo(tokens, "#E4EAE5", 84)}</div>
  </div>
</div>"""
    return moldura(tokens, 13, 13, "Colofão", conteudo)


# ------------------------------------------------------------------ montagem

def montar_html(tokens):
    paginas = [
        p_capa(tokens), p_conceito(tokens), p_construcao(tokens), p_assinaturas(tokens),
        p_protecao(tokens), p_indevidos(tokens), p_cor_institucional(tokens),
        p_cor_funcional(tokens), p_tipografia(tokens), p_icone(tokens),
        p_interface(tokens), p_aplicacoes(tokens), p_colofao(tokens),
    ]
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>BIOSS · Identidade Visual</title>
<style>{css(tokens)}</style>
</head><body>{"".join(paginas)}</body></html>"""


def renderizar(html_path, pdf_path):
    chrome = achar_chromium()
    cmd = [
        chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw", "--virtual-time-budget=15000",
        "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", f"file://{html_path}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not Path(pdf_path).exists():
        sys.stderr.write(r.stderr[-3000:] + "\n")
        raise SystemExit("Falha ao gerar o PDF.")
    return r


def paginas_do_pdf(pdf_path):
    dados = Path(pdf_path).read_bytes()
    return dados.count(b"/Type /Page") - dados.count(b"/Type /Pages") or dados.count(b"/Type/Page")


def conferir_contraste(tokens):
    """
    Trava do build: todo par declarado em tokens.json precisa atingir seu mínimo.
    Reprovou, não gera PDF — paleta inacessível não vira manual.
    """
    pares = tokens.get("acessibilidade", {}).get("pares_obrigatorios", [])
    if not pares:
        raise SystemExit("tokens.json não declara pares de contraste obrigatórios.")

    falhas = []
    print(f"  contraste · {tokens['acessibilidade']['norma']}")
    for p in pares:
        v = contraste(p["frente"], p["fundo"])
        ok = v >= p["minimo"]
        if not ok:
            falhas.append((p, v))
        nivel = "AAA" if v >= 7 else "AA" if v >= 4.5 else "AA-grande" if v >= 3 else "—"
        print(f"    {'ok ' if ok else 'FALHA'} {p['rotulo']:<38} {v:5.2f}:1  "
              f"(mín. {p['minimo']:.1f})  {nivel}")

    if falhas:
        print()
        for p, v in falhas:
            print(f"  ! {p['rotulo']}: {v:.2f}:1 abaixo do mínimo de {p['minimo']:.1f}:1")
        raise SystemExit(f"\nBuild interrompido: {len(falhas)} par(es) de cor reprovaram.")


def main():
    tokens = json.loads((RAIZ / "tokens.json").read_text(encoding="utf-8"))
    SRC.mkdir(exist_ok=True)
    DIST.mkdir(exist_ok=True)

    conferir_contraste(tokens)

    html_path = SRC / "manual.html"
    pdf_path = DIST / "BIOSS-Identidade-Visual.pdf"
    html_path.write_text(montar_html(tokens), encoding="utf-8")

    renderizar(html_path.resolve(), pdf_path.resolve())

    paginas = paginas_do_pdf(pdf_path)
    if paginas != 13:
        raise SystemExit(f"Esperadas 13 páginas, geradas {paginas}.")

    print()
    print(f"  PDF     {pdf_path.relative_to(RAIZ)}")
    print(f"  páginas {paginas}")
    print(f"  tamanho {pdf_path.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
