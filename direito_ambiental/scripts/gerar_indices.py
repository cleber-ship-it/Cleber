#!/usr/bin/env python3
"""Regenera direito_ambiental/indices/ a partir do frontmatter das fichas. Não editar os índices à mão."""
import json, datetime, collections, sys
from _fm import ROOT, iter_fichas, read_fm, rel

OUT = ROOT / "indices"
OUT.mkdir(exist_ok=True)
HOJE = datetime.date.today().isoformat()
AVISO = f"<!-- GERADO AUTOMATICAMENTE por scripts/gerar_indices.py em {HOJE}. Não editar à mão. -->\n"

regs = []
for p in iter_fichas():
    fm, _ = read_fm(p)
    if not fm or "__erro_yaml__" in fm or "tipo_registro" not in fm:
        continue
    fm = dict(fm); fm["_arquivo"] = rel(p)
    regs.append(fm)

normas = [r for r in regs if r["tipo_registro"] == "norma"]
julg = [r for r in regs if r["tipo_registro"] == "julgado"]
muns = [r for r in regs if r["tipo_registro"] == "municipio"]
temas = [r for r in regs if r["tipo_registro"] == "tema"]
pesq = [r for r in regs if r["tipo_registro"] == "pesquisa"]

def ver(r):
    v = r.get("verificacao") or {}
    return f"{v.get('nivel','?')} ({v.get('data_ultima_verificacao') or 'nunca'})"

def link(r):
    return f"[{r.get('id','?')}]({'../' + r['_arquivo']})"

def lin_norma(r):
    return f"| {link(r)} | {r.get('tipo_normativo','')} {r.get('numero','')}/{r.get('ano','')} | {r.get('ente','')}{'/' + str(r['uf']) if r.get('uf') else ''}{' ' + str(r['municipio']) if r.get('municipio') else ''} | {r.get('status_vigencia','')} | {ver(r)} | {str(r.get('ementa',''))[:90]} |"
HN = "| ID | Norma | Ente | Vigência | Verificação | Ementa |\n|---|---|---|---|---|---|\n"

def lin_julg(r):
    return f"| {link(r)} | {r.get('tribunal','')} {r.get('orgao_julgador','')} | {r.get('classe','')} {r.get('numero','')} | {r.get('tipo_precedente','')}{' Tema ' + str(r['tema_numero']) if r.get('tema_numero') else ''} | {r.get('data_julgamento') or ''} | {r.get('situacao_processual','')} | {ver(r)} | {str(r.get('tese',''))[:110]} |"
HJ = "| ID | Tribunal/órgão | Classe/nº | Tipo | Julgamento | Situação | Verificação | Tese |\n|---|---|---|---|---|---|---|---|\n"

def grupo(items, key):
    g = collections.defaultdict(list)
    for r in items:
        vals = r.get(key) or []
        if not isinstance(vals, list): vals = [vals]
        for v in vals or ["(sem classificação)"]:
            g[str(v)].append(r)
    return dict(sorted(g.items()))

def escrever(nome, titulo, corpo):
    (OUT / nome).write_text(AVISO + f"# {titulo}\n\n" + corpo, encoding="utf-8")

# --- INDICE_GERAL
c = collections.Counter
ct_status = c(r.get("status_vigencia","?") for r in normas)
ct_ver = c((r.get("verificacao") or {}).get("nivel","?") for r in regs if r["tipo_registro"] not in ("tema","pesquisa"))
ct_ente = c(r.get("ente","?") for r in normas)
corpo = f"Gerado em {HOJE}.\n\n## Contadores\n"
corpo += f"- Normas: **{len(normas)}** (federal {ct_ente.get('FEDERAL',0)}, estadual {ct_ente.get('ESTADUAL',0)}, municipal {ct_ente.get('MUNICIPAL',0)})\n"
corpo += f"- Julgados/súmulas: **{len(julg)}** | Dossiês municipais: **{len(muns)}** | Temas: **{len(temas)}** | Pesquisas em memória: **{len(pesq)}**\n"
corpo += "- Vigência das normas: " + ", ".join(f"{k} {v}" for k, v in sorted(ct_status.items())) + "\n"
corpo += "- Nível de verificação (normas, julgados e municípios): " + ", ".join(f"{k} {v}" for k, v in sorted(ct_ver.items())) + "\n\n"
corpo += "## Índices disponíveis\n" + "\n".join(f"- [{n}]({n})" for n in [
    "por_assunto.md","por_numero.md","por_ente.md","por_orgao.md","por_municipio.md","por_atividade.md",
    "por_infracao.md","por_status_vigencia.md","jurisprudencia.md","temas.md","memoria.md","normas.json","VOCABULARIO.md"]) + "\n\n"
corpo += "## Todas as normas\n" + HN + "\n".join(lin_norma(r) for r in sorted(normas, key=lambda r: (r.get('ente',''), str(r.get('uf') or ''), -int(r.get('ano') or 0), str(r.get('numero'))))) + "\n"
escrever("INDICE_GERAL.md", "Índice geral do NUCLEO_DIREITO_AMBIENTAL", corpo)

# --- por assunto (normas + julgados + temas)
corpo = ""
todos = normas + julg
for k, rs in grupo(todos, "assuntos").items():
    corpo += f"## {k}\n" + HN.replace("Norma","Norma/Julgado") + "\n".join(
        (lin_norma(r) if r["tipo_registro"]=="norma" else f"| {link(r)} | {r.get('tribunal','')} {r.get('classe','')} {r.get('numero','')} | JURISPRUDÊNCIA | {r.get('situacao_processual','')} | {ver(r)} | {str(r.get('tese',''))[:90]} |") for r in rs) + "\n\n"
    tem = [t for t in temas if k in (t.get("assuntos") or [])]
    if tem: corpo += "Temas: " + ", ".join(link(t) for t in tem) + "\n\n"
escrever("por_assunto.md", "Normas e julgados por assunto", corpo)

# --- por número
corpo = HN + "\n".join(lin_norma(r) for r in sorted(normas, key=lambda r: (r.get('tipo_normativo',''), int(r.get('ano') or 0), str(r.get('numero'))))) + "\n"
escrever("por_numero.md", "Normas por tipo, ano e número", corpo)

# --- por ente / UF
corpo = ""
for ente in ["FEDERAL","ESTADUAL","MUNICIPAL"]:
    rs = [r for r in normas if r.get("ente")==ente]
    if not rs: continue
    corpo += f"## {ente}\n"
    if ente == "FEDERAL":
        corpo += HN + "\n".join(lin_norma(r) for r in rs) + "\n\n"
    else:
        for uf, rr in grupo(rs, "uf").items():
            corpo += f"### {uf}\n" + HN + "\n".join(lin_norma(r) for r in rr) + "\n\n"
escrever("por_ente.md", "Normas por ente federativo", corpo)

# --- por órgão emissor
corpo = ""
for k, rs in grupo(normas, "orgao_emissor").items():
    corpo += f"## {k}\n" + HN + "\n".join(lin_norma(r) for r in rs) + "\n\n"
escrever("por_orgao.md", "Normas por órgão emissor", corpo)

# --- por município (dossiês + normas municipais)
corpo = "## Dossiês municipais\n| ID | Município/UF | Órgão ambiental | Habilitado (impacto local) | Checklist completo | Verificação |\n|---|---|---|---|---|---|\n"
corpo += "\n".join(f"| {link(m)} | {m.get('municipio','')}/{m.get('uf','')} | {m.get('orgao_ambiental') or '?'} | {m.get('habilitado_licenciamento_local')} | {m.get('checklist_completo')} | {ver(m)} |" for m in muns) + "\n\n"
for k, rs in grupo([r for r in normas if r.get("ente")=="MUNICIPAL"], "municipio").items():
    corpo += f"## Normas — {k}\n" + HN + "\n".join(lin_norma(r) for r in rs) + "\n\n"
escrever("por_municipio.md", "Municípios", corpo)

# --- por atividade
corpo = ""
for k, rs in grupo([r for r in normas if r.get("atividades")], "atividades").items():
    corpo += f"## {k}\n" + HN + "\n".join(lin_norma(r) for r in rs) + "\n\n"
escrever("por_atividade.md", "Normas por atividade / tipo de empreendimento", corpo)

# --- infrações
inf = [r for r in todos if "infracoes" in (r.get("assuntos") or []) or "processo_administrativo" in (r.get("assuntos") or [])]
corpo = HN.replace("Norma","Norma/Julgado") + "\n".join((lin_norma(r) if r["tipo_registro"]=="norma" else f"| {link(r)} | {r.get('tribunal','')} {r.get('classe','')} {r.get('numero','')} | JURISPRUDÊNCIA | {r.get('situacao_processual','')} | {ver(r)} | {str(r.get('tese',''))[:90]} |") for r in inf) + "\n"
escrever("por_infracao.md", "Infrações e processo administrativo", corpo)

# --- status vigência
corpo = ""
for k, rs in grupo(normas, "status_vigencia").items():
    corpo += f"## {k} ({len(rs)})\n" + HN + "\n".join(lin_norma(r) for r in rs) + "\n\n"
escrever("por_status_vigencia.md", "Normas por status de vigência", corpo)

# --- jurisprudência
corpo = ""
for k, rs in grupo(julg, "tribunal").items():
    corpo += f"## {k}\n" + HJ + "\n".join(lin_julg(r) for r in sorted(rs, key=lambda r: (r.get('tipo_precedente',''), str(r.get('numero'))))) + "\n\n"
escrever("jurisprudencia.md", "Jurisprudência", corpo)

# --- temas
corpo = "| ID | Tema | Assuntos | Normas centrais | Julgados | Atualizado |\n|---|---|---|---|---|---|\n"
corpo += "\n".join(f"| {link(t)} | {t.get('titulo','')} | {', '.join(t.get('assuntos') or [])} | {len(t.get('normas') or [])} | {len(t.get('julgados') or [])} | {t.get('atualizado_em','')} |" for t in temas) + "\n"
escrever("temas.md", "Temas (mapa semântico)", corpo)

# --- memória
corpo = "| ID | Data | Comando | Questão | Território | Resposta | Confiança | Risco | Validade |\n|---|---|---|---|---|---|---|---|---|\n"
corpo += "\n".join(f"| {link(r)} | {r.get('data','')} | {r.get('comando','')} | {str(r.get('questao',''))[:80]} | {r.get('territorio','')} | {r.get('resposta_direta','')} | {r.get('confianca','')} | {r.get('risco','')} | {r.get('validade_estimada','')} |" for r in sorted(pesq, key=lambda r: str(r.get('data')), reverse=True)) + "\n"
escrever("memoria.md", "Memória de pesquisas", corpo)

# --- JSON
(OUT / "normas.json").write_text(json.dumps(regs, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print(f"Índices gerados em {rel(OUT)}: {len(normas)} normas, {len(julg)} julgados, {len(muns)} municípios, {len(temas)} temas, {len(pesq)} pesquisas.")
