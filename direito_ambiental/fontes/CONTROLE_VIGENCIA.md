# Controle de vigência e de verificação

## 1. Status de vigência (`status_vigencia`)
| Valor | Significado |
|---|---|
| `VIGENTE` | em vigor, sem alteração relevante conhecida ou com alterações já incorporadas na ficha |
| `PARCIALMENTE_VIGENTE` | parte dos dispositivos revogados/derrogados; ficha indica quais |
| `ALTERADA` | vigente, mas com alteração recente ainda não totalmente incorporada na ficha (ATENÇÃO) |
| `REVOGADA` | revogada expressa ou tacitamente; indicar norma revogadora e data |
| `SUSPENSA` | eficácia suspensa (cautelar judicial, decreto legislativo etc.) |
| `EFICACIA_QUESTIONADA` | vigente, mas com impugnação relevante (ADI, ADPF, incidente) sem decisão |
| `EM_JULGAMENTO` | ação de controle concentrado ou tese repetitiva pendente que pode alterar a aplicação |
| `SUBSTITUIDA` | substituída por norma posterior que rege integralmente a matéria |
| `PENDENTE_REGULAMENTACAO` | vigente, mas depende de regulamento ainda não editado para dispositivos relevantes |

## 2. Nível de verificação (`verificacao.nivel`)
| Valor | Significado | Quando é atribuído |
|---|---|---|
| `FONTE_PRIMARIA` | texto conferido diretamente na fonte oficial (Planalto, DOU, AL-RS, DOE, DOM, portal do tribunal) na data indicada | leitura direta (WebFetch/browser/PDF oficial) |
| `INDIRETA` | existência/status confirmados por fonte secundária confiável (notícia oficial de tribunal/casa legislativa, escritório, portal jurídico, WebSearch) sem leitura do texto oficial | quando o acesso direto está bloqueado |
| `NAO_VERIFICADA` | registro feito a partir do conhecimento do modelo, sem confirmação externa | seed inicial; SEMPRE tratar como hipótese a confirmar |

Campos obrigatórios em `verificacao`: `nivel`, `data_ultima_verificacao` (ISO ou null), `metodo`
(`fonte_primaria` | `websearch_secundaria` | `memoria_modelo` | `documento_fornecido_usuario`), `observacao`.

## 3. Regras de uso
- Norma `NAO_VERIFICADA` pode ser citada apenas com a ressalva expressa "não verificada na fonte oficial nesta data" e rebaixa a confiança para no máximo MÉDIA.
- Norma com `data_ultima_verificacao` > 180 dias (normas) ou > 365 dias (julgados) é considerada **VENCIDA** pelo `validar_base.py` e deve ser reverificada antes de fundamentar manifestação relevante.
- `ALTERADA`, `EFICACIA_QUESTIONADA`, `EM_JULGAMENTO`: exigem menção expressa do risco na resposta.
- Qualquer mudança de status é registrada no `CHANGELOG_JURIDICO_AMBIENTAL.md` com motivo e fonte.

## 4. Campos mínimos de uma ficha de norma
número; tipo normativo; data; ente federativo; órgão emissor; ementa/assunto; dispositivos relevantes;
alterações posteriores (`alterada_por`); norma revogadora (`revogada_por`); fonte; URL oficial;
data da última verificação. Ver `templates/FICHA_NORMA.md`.

## 5. Ambiente de execução
Em 2026-09-11 constatou-se neste ambiente remoto: acesso HTTP direto (curl/WebFetch) BLOQUEADO para
planalto.gov.br, camara.leg.br, stf.jus.br, stj.jus.br, al.rs.gov.br, sema.rs.gov.br, fepam.rs.gov.br,
conama.mma.gov.br e legisweb.com.br; `WebSearch` FUNCIONA (retorna resumos e URLs). Consequência:
o nível máximo atingível aqui é `INDIRETA`, salvo se o usuário fornecer o texto oficial
(`documento_fornecido_usuario`) ou a política de rede do ambiente for ajustada. Em ambiente local
(Claude Code desktop/CLI com rede aberta) o alvo é `FONTE_PRIMARIA`.
