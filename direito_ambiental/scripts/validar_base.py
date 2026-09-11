#!/usr/bin/env python3
"""Valida a integridade da base do NUCLEO_DIREITO_AMBIENTAL.
Uso: validar_base.py [--resumo] [--vencidas] [--estrito]
Sai com código 1 se houver ERROS (não com avisos), salvo --estrito (avisos também falham)."""
import sys, re, datetime, pathlib
from _fm import ROOT, REPO, iter_fichas, read_fm, rel

args = set(sys.argv[1:])
HOJE = datetime.date.today()
STATUS = {"VIGENTE","PARCIALMENTE_VIGENTE","ALTERADA","REVOGADA","SUSPENSA","EFICACIA_QUESTIONADA","EM_JULGAMENTO","SUBSTITUIDA","PENDENTE_REGULAMENTACAO"}
NIVEIS = {"FONTE_PRIMARIA","INDIRETA","NAO_VERIFICADA"}
METODOS = {"fonte_primaria","websearch_secundaria","memoria_modelo","documento_fornecido_usuario"}
CONF = {"ALTA","MEDIA","BAIXA"}
ENTES = {"FEDERAL","ESTADUAL","MUNICIPAL"}
REQ = {
 "norma": ["id","tipo_normativo","numero","ano","ente","orgao_emissor","ementa","assuntos","status_vigencia","fonte_oficial_url","verificacao","confianca_registro"],
 "julgado": ["id","tribunal","classe","numero","tipo_precedente","tese","assuntos","situacao_processual","fonte_oficial_url","verificacao","confianca_registro"],
 "municipio": ["id","municipio","uf","orgao_ambiental","prioridade","checklist_completo","verificacao"],
 "tema": ["id","titulo","assuntos","normas","julgados","atualizado_em"],
 "pesquisa": ["id","data","comando","questao","temas","normas_citadas","julgados_citados","resposta_direta","confianca","risco","nivel_verificacao_predominante","revisao_adversarial","validade_estimada"],
 "perfil_uf": ["id","uf","nome","orgao_licenciador","conselho_estadual","orgao_recursos_hidricos","portal_legislacao","prioridade","normas_centrais","verificacao"],
}
VENC_NORMA, VENC_JULG = 180, 365
erros, avisos, ids = [], [], {}
regs = []
vocab = set()
vp = ROOT / "indices" / "VOCABULARIO.md"
if vp.exists():
    vocab = set(re.findall(r"^\| `([a-z0-9_]+)`", vp.read_text(encoding="utf-8"), re.M))

for p in iter_fichas():
    fm, body = read_fm(p)
    r = rel(p)
    if fm is None:
        erros.append(f"{r}: sem frontmatter YAML"); continue
    if "__erro_yaml__" in fm:
        erros.append(f"{r}: YAML inválido: {fm['__erro_yaml__']}"); continue
    t = fm.get("tipo_registro")
    if t not in REQ:
        erros.append(f"{r}: tipo_registro inválido: {t}"); continue
    for k in REQ[t]:
        if k not in fm or fm[k] in (None, "", []) and k not in ("normas","julgados","normas_citadas","julgados_citados","assuntos"):
            erros.append(f"{r}: campo obrigatório ausente/vazio: {k}")
    i = fm.get("id")
    if i:
        if i in ids: erros.append(f"{r}: ID duplicado {i} (também em {ids[i]})")
        ids[i] = r
        if not re.match(r"^[A-Z0-9][A-Z0-9\-]+$", str(i)): erros.append(f"{r}: ID fora do padrão (maiúsculas, dígitos e hífens): {i}")
    if t == "norma":
        if fm.get("status_vigencia") not in STATUS: erros.append(f"{r}: status_vigencia inválido: {fm.get('status_vigencia')}")
        if fm.get("ente") not in ENTES: erros.append(f"{r}: ente inválido: {fm.get('ente')}")
        if fm.get("ente") != "FEDERAL" and not fm.get("uf"): erros.append(f"{r}: norma {fm.get('ente')} sem uf")
        if fm.get("ente") == "MUNICIPAL" and not fm.get("municipio"): erros.append(f"{r}: norma MUNICIPAL sem municipio")
        if fm.get("status_vigencia") == "REVOGADA" and not fm.get("revogada_por"): erros.append(f"{r}: REVOGADA sem revogada_por")
        if fm.get("status_vigencia") == "ALTERADA" and not fm.get("alterada_por"): avisos.append(f"{r}: ALTERADA sem alterada_por")
        if fm.get("confianca_registro") not in CONF: erros.append(f"{r}: confianca_registro inválida")
    if t == "julgado" and fm.get("confianca_registro") not in CONF: erros.append(f"{r}: confianca_registro inválida")
    v = fm.get("verificacao") if t not in ("tema","pesquisa") else None
    if v is not None:
        if not isinstance(v, dict): erros.append(f"{r}: verificacao deve ser mapa"); v = {}
        if v.get("nivel") not in NIVEIS: erros.append(f"{r}: verificacao.nivel inválido: {v.get('nivel')}")
        if v.get("metodo") not in METODOS: erros.append(f"{r}: verificacao.metodo inválido: {v.get('metodo')}")
        d = v.get("data_ultima_verificacao")
        if d is not None:
            try:
                d = datetime.date.fromisoformat(str(d))
                lim = VENC_JULG if t == "julgado" else VENC_NORMA
                if (HOJE - d).days > lim: avisos.append(f"{r}: verificação VENCIDA ({d}, {(HOJE-d).days} dias)")
            except ValueError: erros.append(f"{r}: data_ultima_verificacao inválida: {d}")
        else:
            if v.get("nivel") != "NAO_VERIFICADA": erros.append(f"{r}: nível {v.get('nivel')} exige data_ultima_verificacao")
            if "--vencidas" in args: avisos.append(f"{r}: NUNCA verificada")
        if v.get("nivel") == "NAO_VERIFICADA" and v.get("metodo") not in ("memoria_modelo",): avisos.append(f"{r}: NAO_VERIFICADA com método {v.get('metodo')}")
    for a in fm.get("assuntos") or []:
        if vocab and a not in vocab: avisos.append(f"{r}: assunto fora do vocabulário: {a}")
    # aspas no corpo sem "conferida" -> aviso leve para fichas NAO_VERIFICADA
    if t == "norma" and v and v.get("nivel") == "NAO_VERIFICADA" and re.search(r"\| *SIM *\|", body):
        avisos.append(f"{r}: marca redação 'conferida' (SIM) mas ficha NAO_VERIFICADA")
    regs.append((r, fm))

# referências cruzadas
for r, fm in regs:
    refs = []
    for k in ("alterada_por","altera","revoga","normas_relacionadas","normas","julgados","normas_citadas","julgados_citados","normas_centrais"):
        vals = fm.get(k) or []
        if isinstance(vals, list): refs += [x for x in vals if isinstance(x, str)]
    if fm.get("revogada_por"): refs.append(fm["revogada_por"])
    if fm.get("superado_por"): refs.append(fm["superado_por"])
    for x in refs:
        if re.match(r"^[A-Z]{2,}-[A-Z0-9\-]+$", x) and x not in ids:
            avisos.append(f"{r}: referência a ID inexistente: {x}")

# estrutura do Claude Code
ag = REPO / ".claude" / "agents"
esperados = ["coordenador-direito-ambiental","direito-ambiental-estados","consultor-tecnico-ambiental","revisor-juridico-adversarial","verificador-fontes-normativas","direito-ambiental-federal","direito-ambiental-rs","direito-ambiental-municipal","licenciamento-ambiental","flora-app-mata-atlantica","infracoes-processo-administrativo","responsabilidade-civil-ambiental","recursos-hidricos-saneamento","urbanistico-ambiental","jurisprudencia-ambiental"]
for n in esperados:
    f = ag / f"{n}.md"
    if not f.exists(): erros.append(f"agente ausente: {rel(f) if f.exists() else f}")
    else:
        fm, _ = read_fm(f)
        if not fm or fm.get("name") != n or not fm.get("description"): erros.append(f".claude/agents/{n}.md: frontmatter inválido (name/description)")
for s in ["direito-ambiental","pesquisa-juridica","auditar-juridico","atualizar-direito-ambiental","registrar-norma"]:
    f = REPO / ".claude" / "skills" / s / "SKILL.md"
    if not f.exists(): erros.append(f"skill ausente: {s}")
    else:
        fm, _ = read_fm(f)
        if not fm or fm.get("name") != s: erros.append(f"skill {s}: frontmatter inválido")
for f in ["CLAUDE.md",".claude/settings.json","direito_ambiental/README.md","direito_ambiental/PROTOCOLO_PESQUISA.md","direito_ambiental/CHANGELOG_JURIDICO_AMBIENTAL.md","direito_ambiental/STATUS.md","direito_ambiental/fontes/CONTROLE_VIGENCIA.md","direito_ambiental/fontes/FONTES_OFICIAIS.md","direito_ambiental/REGRAS_COMUNS_AGENTES.md","direito_ambiental/integracao/PROTOCOLO_INTEGRACAO.md","direito_ambiental/memoria/INDICE.md"]:
    if not (REPO / f).exists(): erros.append(f"arquivo permanente ausente: {f}")
# links internos em arquivos md de referência (caminhos relativos ao repo citados entre crases)
for f in ["CLAUDE.md","direito_ambiental/README.md"]:
    txt = (REPO / f).read_text(encoding="utf-8") if (REPO / f).exists() else ""
    for m in re.findall(r"`((?:direito_ambiental|\.claude)/[A-Za-z0-9_\-./{}]+)`", txt):
        if "{" in m or m.endswith("/"): continue
        if not (REPO / m).exists(): avisos.append(f"{f}: caminho citado não existe: {m}")

n_reg = len(regs)
if "--resumo" in args:
    print(f"[validar_base] {n_reg} registros | {len(erros)} erros | {len(avisos)} avisos")
    for e in erros[:5]: print("  ERRO:", e)
    sys.exit(0)
for e in erros: print("ERRO:", e)
for a in avisos: print("AVISO:", a)
print(f"\n{n_reg} registros validados | {len(erros)} erros | {len(avisos)} avisos")
sys.exit(1 if erros or ("--estrito" in args and avisos) else 0)
