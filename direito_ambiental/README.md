# NUCLEO_DIREITO_AMBIENTAL — Manual

Estrutura permanente de conhecimento jurídico ambiental brasileiro da Biogênese Ambiental.
Não é um "agente de respostas": é uma base rastreável (normas, julgados, temas, memória) operada por
agentes especializados, com controle de vigência, verificação de fontes e revisão adversarial.

Criado em 2026-09-11. Estado atual: `STATUS.md`. Alterações: `CHANGELOG_JURIDICO_AMBIENTAL.md`.

## Mapa da estrutura

```
direito_ambiental/
├── README.md                         este manual
├── PROTOCOLO_PESQUISA.md             padrão obrigatório de pesquisa (16 passos), formatos, confiança, risco
├── STATUS.md                         data da última atualização, contadores, pendências
├── CHANGELOG_JURIDICO_AMBIENTAL.md   log de novidades, alterações, revogações, correções
├── PENDENTES_DE_LEVANTAMENTO.md      normas/dados citados de memória que ainda NÃO podem virar ficha
├── REGRAS_COMUNS_AGENTES.md          regras lidas por todos os agentes (fora de .claude/agents para não ser lido como agente)
├── fontes/
│   ├── FONTES_OFICIAIS.md            catálogo de fontes primárias (URLs) por ente/órgão
│   └── CONTROLE_VIGENCIA.md          taxonomia de status de vigência e níveis de verificação
├── federal/                          fichas de normas federais (1 arquivo por norma)
├── estadual/rs/                      fichas RS (prioritário)
├── estadual/<uf>/PERFIL.md + fichas  14 UFs perfiladas (sc pr sp mg mt ms go rj pe pb es ce ba pi); outros/README.md para novas UFs
├── municipal/<uf>/<municipio>.md     dossiês (RS: 5 da Serra Gaúcha; BA: Salvador, Simões Filho, Candeias; PI: Teresina)
├── jurisprudencia/{stf,stj,trf,tj,sumulas}/  fichas de julgados e súmulas
├── temas/                            sínteses por tema (ponte semântica: pergunta → normas → julgados)
├── memoria/pesquisas/                registros de pesquisas/pareceres já realizados + INDICE.md
├── integracao/                       protocolo de consulta entre núcleo jurídico e agentes técnicos
├── templates/                        FICHA_NORMA, FICHA_JULGADO, MUNICIPIO, RESPOSTA_JURIDICA, MATRIZ_CASO,
│                                     ESTRATEGIA_JURIDICA, AUDITORIA, PESQUISA_MEMORIA, AGENTE_TECNICO
├── indices/                          GERADOS por scripts (não editar à mão): por assunto, número, ente,
│                                     órgão, município, atividade, infração, jurisprudência, normas.json
└── scripts/
    ├── gerar_indices.py              lê o frontmatter YAML das fichas e regenera indices/
    ├── validar_base.py               valida campos, status, IDs, referências cruzadas, verificações vencidas
    ├── registrar_verificacao.py      atualiza verificacao/status de uma ficha e registra no changelog
    └── status_nucleo.sh              resumo exibido no início da sessão (hook SessionStart)
```

## Agentes (`.claude/agents/`)

| Agente | Papel |
|---|---|
| `coordenador-direito-ambiental` | INTEGRADOR: recebe a questão, aciona especialistas, consolida, elimina duplicidades/contradições/citações não comprovadas, garante revisão adversarial |
| `revisor-juridico-adversarial` | Tenta DESTRUIR a conclusão: norma esquecida, exceção, revogação, jurisprudência contrária, competência, argumento do órgão/MP/parte contrária |
| `direito-ambiental-federal` | CF, PNMA, Lei 9.605, Dec. 6.514, Código Florestal, Mata Atlântica, LC 140, CONAMA, recursos hídricos, resíduos, fauna, flora |
| `direito-ambiental-rs` | Código Estadual (Lei 15.434/2020), CONSEMA, FEPAM, SEMA, DRHS, CRH, municipalização, enquadramentos |
| `direito-ambiental-estados` | Demais UFs (SC, PR, SP, MG, MT, MS, GO, RJ, PE, PB, ES, CE, BA, PI e outras) a partir de `estadual/<uf>/PERFIL.md` |
| `direito-ambiental-municipal` | Localiza e interpreta legislação municipal (checklist obrigatório de 18 itens) |
| `licenciamento-ambiental` | LP/LI/LO/LOR, corretivo, renovação, condicionantes, competência, enquadramento, estudos (EIA/RIMA, RCA, PCA, RAS, PRAD), Lei 15.190/2025 |
| `flora-app-mata-atlantica` | Lei 11.428, Dec. 6.660, Lei 12.651, APP, RL, estágio sucessional, supressão, compensação, SINAFLOR, espécies |
| `infracoes-processo-administrativo` | Lei 9.605, Dec. 6.514, autos, multas, embargo, defesa, recurso, prescrição, dosimetria, nulidades |
| `responsabilidade-civil-ambiental` | dano, responsabilidade objetiva, risco integral, propter rem, reparação in natura, solidariedade, imprescritibilidade |
| `recursos-hidricos-saneamento` | outorga, intervenção, efluentes, APP hídrica, nascentes, ETE/ETA, enquadramento, CNRH, CRH/RS |
| `urbanistico-ambiental` | Estatuto da Cidade, Lei 6.766, APP urbana, plano diretor, REURB, área urbana consolidada |
| `jurisprudencia-ambiental` | localiza, autentica e analisa precedentes; superação/distinção |
| `verificador-fontes-normativas` | SUBAGENTE: confere existência, vigência, redação e URL oficial de cada citação; atribui nível de verificação |
| `consultor-tecnico-ambiental` | Técnico GENÉRICO (substituto até haver especialistas por área): confirma/refuta/declara indeterminada a premissa técnica no formato RESPOSTA_TECNICA |

## Comandos (`.claude/skills/`)
`/direito-ambiental`, `/pesquisa-juridica`, `/auditar-juridico`, `/atualizar-direito-ambiental`, `/registrar-norma`.

## Fluxo mínimo de uma consulta
1. Coordenador identifica FATO, TERRITÓRIO (município/UF), ATIVIDADE, ÓRGÃO COMPETENTE, TEMA.
2. Consulta `indices/` e `temas/` (memória como índice).
3. Aciona especialistas federal → estadual → municipal → temáticos → jurisprudência.
4. `verificador-fontes-normativas` confere cada citação e atribui nível de verificação.
5. `revisor-juridico-adversarial` ataca a conclusão.
6. Coordenador consolida no formato padrão, com CONFIANÇA, RISCO e DATA DAS FONTES.
7. Pesquisa relevante é registrada em `memoria/pesquisas/` e indexada.

## Princípios não negociáveis
Ver `CLAUDE.md` (raiz) — regras 1 a 12. Em especial: NÃO INVENTAR LEGISLAÇÃO; MEMÓRIA ≠ VERDADE ATUAL;
LOCALIZE → CONFIRME → COMPARE → VERIFIQUE VIGÊNCIA → ANALISE COMPETÊNCIA → PROCURE EXCEÇÕES →
PROCURE JURISPRUDÊNCIA → TESTE A TESE CONTRÁRIA → SÓ ENTÃO CONCLUA.
