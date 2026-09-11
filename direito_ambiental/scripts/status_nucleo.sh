#!/usr/bin/env bash
# Resumo do NUCLEO_DIREITO_AMBIENTAL exibido no início da sessão (hook SessionStart).
# Nunca falha a sessão: qualquer erro é silenciado e o script retorna 0.
set +e
ROOT="$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd)"
DA="$ROOT/direito_ambiental"
[ -d "$DA" ] || exit 0
ULT=$(grep -m1 -oE 'Última atualização geral[^:]*:\*\* [0-9]{4}-[0-9]{2}-[0-9]{2}' "$DA/STATUS.md" 2>/dev/null | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
HOJE=$(date +%F)
echo "[NUCLEO_DIREITO_AMBIENTAL] ativo. Última atualização geral: ${ULT:-desconhecida}. Hoje: $HOJE."
if [ -n "$ULT" ] && command -v python3 >/dev/null 2>&1; then
  DIAS=$(python3 - "$ULT" "$HOJE" <<'PY' 2>/dev/null
import sys, datetime as d
a=d.date.fromisoformat(sys.argv[1]); b=d.date.fromisoformat(sys.argv[2]); print((b-a).days)
PY
)
  if [ -n "$DIAS" ] && [ "$DIAS" -gt 30 ]; then
    echo "[NUCLEO_DIREITO_AMBIENTAL] ATENÇÃO: ${DIAS} dias sem /atualizar-direito-ambiental. MEMÓRIA ≠ VERDADE ATUAL: reverificar vigência antes de manifestações relevantes."
  fi
fi
if command -v python3 >/dev/null 2>&1 && [ -f "$DA/scripts/validar_base.py" ]; then
  python3 "$DA/scripts/validar_base.py" --resumo 2>/dev/null | head -5
fi
echo "[NUCLEO_DIREITO_AMBIENTAL] Comandos: /direito-ambiental, /pesquisa-juridica, /auditar-juridico, /atualizar-direito-ambiental, /registrar-norma. Regras: CLAUDE.md."
exit 0
