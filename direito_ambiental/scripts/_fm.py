"""Utilitários compartilhados: leitura/escrita de frontmatter YAML das fichas."""
import re, sys, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]          # direito_ambiental/
REPO = ROOT.parent
FICHA_DIRS = ["federal", "estadual", "municipal", "jurisprudencia", "temas", "memoria"]
FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.S)

def iter_fichas():
    for d in FICHA_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.md")):
            if p.name.startswith("_") or p.name.upper() in ("README.MD", "INDICE.MD"):
                continue
            yield p

def read_fm(path):
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return None, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return {"__erro_yaml__": str(e)}, m.group(2)
    return data, m.group(2)

def write_fm(path, data, body):
    fm = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    path.write_text(f"---\n{fm}---\n{body.lstrip(chr(10))}", encoding="utf-8")

def rel(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")
