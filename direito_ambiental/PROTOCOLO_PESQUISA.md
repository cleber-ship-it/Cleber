# Protocolo obrigatório de pesquisa jurídica ambiental

Aplica-se a toda questão jurídica ambiental relevante. Consultas triviais podem abreviar etapas, mas
NUNCA as etapas 9 (vigência), 15 (revisão adversarial, quando houver manifestação relevante) e a
declaração de confiança/data das fontes.

## A. Os 16 passos
1. **Identificar o fato** (o que ocorreu / o que se pretende; datas; área; volumes).
2. **Identificar o território** (município, UF, zona urbana/rural, bioma, bacia, UC/zona de amortecimento).
3. **Identificar a atividade** (CNAE/CODRAM quando aplicável; porte; potencial poluidor).
4. **Identificar o órgão competente** (LC 140/2011; CONSEMA 372/2018 no RS; convênios; licença existente).
5. **Identificar o tema jurídico** (licenciamento, infração, responsabilidade civil, flora, hídrico, urbanístico...).
6. **Buscar legislação federal** (CF → LC → lei → decreto → resolução → IN/portaria).
7. **Buscar legislação estadual** (Constituição Estadual, Código, decretos, CONSEMA/CRH, FEPAM/SEMA/DRHS).
8. **Buscar legislação municipal** (checklist de 18 itens em `templates/MUNICIPIO.md`).
9. **Verificar vigência** de CADA norma citada (`fontes/CONTROLE_VIGENCIA.md`).
10. **Verificar alterações** posteriores (redação atual vs. original; dispositivos revogados).
11. **Procurar jurisprudência** (STF → STJ → TRF4/TJRS → outros), autenticando cada julgado.
12. **Procurar entendimento administrativo** (pareceres, notas técnicas, INs, prática do órgão).
13. **Confrontar normas** (hierarquia, competência, especialidade, cronologia, territorialidade, norma mais protetiva).
14. **Analisar exceções** (utilidade pública, interesse social, baixo impacto, área consolidada, prazos, anistias, dispensas).
15. **Executar revisão adversarial** (`revisor-juridico-adversarial`).
16. **Emitir conclusão** no formato padrão.

## B. Hierarquia normativa a considerar
CF → tratados internalizados → leis complementares → leis ordinárias → decretos → resoluções →
portarias → instruções normativas → normas estaduais → normas municipais → atos administrativos →
licenças → condicionantes → termos administrativos específicos.
Sempre analisar competência legislativa (CF 24, VI e VIII; 30, I e II; 22), administrativa (CF 23, III,
VI, VII; LC 140/2011), especialidade, territorialidade, cronologia, hierarquia, conflito e norma mais
protetiva (com a ressalva de que "mais protetivo" não é critério automático — ver STF Tema 145).

## C. Distinções obrigatórias em toda resposta
| Camada | O que é |
|---|---|
| TEXTO EXPRESSO DA NORMA | o que está literalmente escrito (citar redação) |
| INTERPRETAÇÃO JURÍDICA | conclusão extraída da norma |
| JURISPRUDÊNCIA | como tribunais decidem (precedente identificado) |
| PRÁTICA ADMINISTRATIVA | como o órgão costuma aplicar |
| ENTENDIMENTO TÉCNICO | conclusão técnico-ambiental que interfere no enquadramento |

| Natureza do comando | Significado |
|---|---|
| OBRIGAÇÃO LEGAL | comando normativo vinculante |
| ENTENDIMENTO JURISPRUDENCIAL | interpretação judicial consolidada ou relevante |
| EXIGÊNCIA ADMINISTRATIVA | o órgão costuma/está exigindo |
| BOA PRÁTICA | recomendável, não obrigatório |

## D. Formato padrão de resposta
Ver `templates/RESPOSTA_JURIDICA.md`: QUESTÃO / RESPOSTA DIRETA / FUNDAMENTO LEGAL / INTERPRETAÇÃO /
JURISPRUDÊNCIA / APLICAÇÃO AO CASO / RISCO JURÍDICO / ARGUMENTO CONTRÁRIO / CONCLUSÃO.

## E. Citações
Norma: nome, número, artigo, parágrafo, inciso, data, link oficial.
Julgado: número do processo, tribunal, órgão julgador, relator, data de julgamento, link oficial.
Proibido "segundo o STJ" sem identificar o precedente. Se não for possível identificar: dizer que não foi
possível e não usar como fundamento.

## F. Controle de confiança
- **ALTA**: norma clara e vigente verificada (FONTE_PRIMARIA ou INDIRETA recente), jurisprudência convergente, sem conflito relevante.
- **MÉDIA**: norma clara mas verificação antiga/indireta, OU jurisprudência dividida, OU dependência de premissa técnica não confirmada.
- **BAIXA**: norma não verificada, conflito normativo, lacuna, dependência de legislação municipal não levantada, ou jurisprudência inexistente/superada.
Registrar os fatores que rebaixaram a confiança.

## G. Risco jurídico
BAIXO / MODERADO / ELEVADO / MUITO ELEVADO — sempre com o cenário adverso descrito (o que o órgão, o MP
ou a parte contrária alegaria).

## H. Casos práticos — matriz
FATO → NORMA → REQUISITO LEGAL → EVIDÊNCIA DISPONÍVEL → ATENDIMENTO/NÃO ATENDIMENTO → RISCO → ESTRATÉGIA
(`templates/MATRIZ_CASO.md`).

## I. Estratégia jurídica (defesas, recursos, argumentos)
TESE PRINCIPAL / TESE SUBSIDIÁRIA / ARGUMENTO ADVERSO / CONTRA-ARGUMENTAÇÃO / RISCO
(`templates/ESTRATEGIA_JURIDICA.md`). O núcleo é crítico: se a tese do usuário for fraca, dizer.

## J. Pesquisa semântica
Perguntas conceituais ("onde está escrito que a recuperação tem de ser no mesmo local?") NÃO se
resolvem por busca literal. Começar por `temas/` (mapa conceito → normas → julgados), expandir para
sinônimos e institutos correlatos (dever de reparar, reparação in natura, restitutio in integrum,
recuperação de APP, propter rem...), e então separar: expresso / interpretação / jurisprudência.

## L. O que é "manifestação relevante" (critério objetivo)
RELEVANTE = qualquer conclusão que será usada fora da conversa: perante órgão ambiental, MP, juízo, cliente, em
parecer, defesa, recurso, TAC/TC, resposta a notificação, relatório técnico ou e-mail com orientação. Exige fluxo
completo (especialistas → verificador → revisor adversarial → coordenador). TRIVIAL = orientação interna imediata,
sem uso externo, integralmente respondida por ficha verificada; ainda assim mantém formato, confiança e data das
fontes e declara "sem revisão adversarial". Na dúvida, é RELEVANTE.

## K. Data de corte e atualização
Toda análise informa `DATA_DAS_FONTES` e o nível de verificação. Se a análise tem impacto jurídico
significativo e a fonte não foi conferida recentemente (> 180 dias para normas, > 365 para julgados, NUNCA verificada,
ou qualquer prazo se houver notícia de alteração): ATUALIZAR ANTES DE CONCLUIR, ou declarar a
impossibilidade e rebaixar a confiança.
