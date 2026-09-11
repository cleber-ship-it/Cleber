#!/usr/bin/env python3
"""Atualiza o bloco `verificacao` (e opcionalmente status/URL) de uma ficha e registra no CHANGELOG quando
o status muda ou quando --changelog for passado.
Uso: registrar_verificacao.py --id ID --nivel NIVEL --metodo METODO [--status STATUS] [--fonte URL]
     [--obs TEXTO] [--data AAAA-MM-DD] [--changelog] [--impacto TEXTO] [--area TEXTO]"""
import argparse, datetime, sys
from _fm import ROOT, iter_fichas, read_fm, write_fm, rel

ap = argparse.ArgumentParser()
ap.add_argument("--id", required=True); ap.add_argument("--nivel", required=True, choices=["FONTE_PRIMARIA","INDIRETA","NAO_VERIFICADA"])
ap.add_argument("--metodo", required=True, choices=["fonte_primaria","websearch_secundaria","memoria_modelo","documento_fornecido_usuario"])
ap.add_argument("--status"); ap.add_argument("--fonte"); ap.add_argument("--obs", default=""); ap.add_argument("--data", default=datetime.date.today().isoformat())
ap.add_argument("--changelog", action="store_true"); ap.add_argument("--impacto", default="(preencher)"); ap.add_argument("--area", default="(preencher)")
a = ap.parse_args()

alvo = None
for p in iter_fichas():
    fm, body = read_fm(p)
    if fm and fm.get("id") == a.id:
        alvo = (p, fm, body); break
if not alvo:
    sys.exit(f"ID não encontrado: {a.id}")
p, fm, body = alvo
antigo = fm.get("status_vigencia") or fm.get("situacao_processual")
v = fm.get("verificacao") or {}
v.update({"nivel": a.nivel, "data_ultima_verificacao": None if a.nivel == "NAO_VERIFICADA" else a.data, "metodo": a.metodo, "observacao": a.obs or v.get("observacao","")})
fm["verificacao"] = v
mudou_status = False
if a.status:
    chave = "status_vigencia" if fm.get("tipo_registro") == "norma" else "situacao_processual"
    mudou_status = fm.get(chave) != a.status
    fm[chave] = a.status
if a.fonte: fm["fonte_oficial_url"] = a.fonte
# histórico na tabela do corpo
linha = f"| {a.data} | {a.nivel} | {a.metodo} | {a.obs or ('status ' + str(a.status) if a.status else 'reverificação')} |"
if "## Histórico de verificação" in body:
    idx = body.index("## Histórico de verificação")
    body = body[:idx].rstrip("\n") + "\n" + body[idx:].rstrip("\n") + "\n" + linha + "\n"
else:
    body = body.rstrip("\n") + "\n\n## Histórico de verificação\n| Data | Nível | Método | Resultado |\n|---|---|---|---|\n" + linha + "\n"
write_fm(p, fm, body)
print(f"Atualizado {rel(p)}: nível={a.nivel}, data={v['data_ultima_verificacao']}, status={a.status or '(inalterado)'}")

if mudou_status or a.changelog:
    ch = ROOT / "CHANGELOG_JURIDICO_AMBIENTAL.md"
    txt = ch.read_text(encoding="utf-8")
    bloco = (f"\n## {a.data} — {a.id}: {'mudança de status ' + str(antigo) + ' → ' + str(a.status) if mudou_status else 'verificação registrada'}\n"
             f"- DATA: {a.data} | DATA DO ATO: (preencher)\n- NORMA/JULGADO: {a.id} ({rel(p)})\n"
             f"- ALTERAÇÃO: {a.obs or '(preencher)'}\n- IMPACTO: {a.impacto}\n- ÁREA AFETADA: {a.area}\n"
             f"- PROCESSOS/CLIENTES POTENCIALMENTE AFETADOS: (preencher)\n- FONTE OFICIAL: {a.fonte or fm.get('fonte_oficial_url','')} | NÍVEL DE VERIFICAÇÃO: {a.nivel}\n"
             f"- RESPONSÁVEL: registrar_verificacao.py\n")
    marca = "\n---\n"
    if marca in txt:
        i = txt.index(marca) + len(marca)
        txt = txt[:i] + bloco + txt[i:]
    else:
        txt += bloco
    ch.write_text(txt, encoding="utf-8")
    print("Entrada adicionada ao CHANGELOG.")
