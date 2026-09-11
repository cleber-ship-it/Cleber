# Base de trabalho — Biogênese Ambiental

Repositório de trabalho da Biogênese Ambiental (consultoria ambiental, Serra Gaúcha/RS).
Contém entregáveis técnicos avulsos (ex.: `simulador-financiamento-imobiliario.html`) e o
**NÚCLEO PERMANENTE DE DIREITO AMBIENTAL** descrito abaixo.

## NUCLEO_DIREITO_AMBIENTAL — regras obrigatórias

Diretório: `direito_ambiental/` (conhecimento) + `.claude/agents/` (agentes) + `.claude/skills/` (comandos).
Manual completo: `direito_ambiental/README.md`. Protocolo de pesquisa: `direito_ambiental/PROTOCOLO_PESQUISA.md`.

### Quando acionar
Qualquer questão que envolva legislação, licenciamento, infração, responsabilidade, competência
ou norma ambiental (federal, estadual, municipal) DEVE passar pelo núcleo. Use os comandos:

| Comando | Uso |
|---|---|
| `/direito-ambiental <pergunta>` | Consulta rápida com acionamento automático dos especialistas |
| `/pesquisa-juridica <tema>` | Investigação ampliada (legislação, regulamentos, jurisprudência, histórico) |
| `/auditar-juridico <arquivo ou texto>` | Auditoria de documento (citações, vigência, lógica, argumentos adversos) |
| `/atualizar-direito-ambiental [escopo]` | Rotina de atualização normativa e jurisprudencial |
| `/registrar-norma` | Cadastrar/atualizar ficha de norma ou julgado na base |

### Regras invioláveis (valem para TODOS os agentes desta base)
1. **NÃO INVENTAR LEGISLAÇÃO.** Proibido inventar artigo, inciso, parágrafo, resolução, súmula,
   acórdão, número de processo ou atribuir texto inexistente a uma norma. Sem confirmação: declare
   a incerteza. Nunca preencher lacuna com suposição.
2. **MEMÓRIA ≠ VERDADE ATUAL.** As fichas em `direito_ambiental/` são ÍNDICE, não autoridade.
   Antes de usar informação sensível à vigência, verificar a fonte oficial (ou declarar que não foi
   possível). Toda ficha traz `verificacao.nivel` e `data_ultima_verificacao`; respeite-os.
3. **Separar sempre:** TEXTO EXPRESSO DA NORMA / INTERPRETAÇÃO / JURISPRUDÊNCIA / PRÁTICA
   ADMINISTRATIVA / ENTENDIMENTO TÉCNICO. E: OBRIGAÇÃO LEGAL / ENTENDIMENTO JURISPRUDENCIAL /
   EXIGÊNCIA ADMINISTRATIVA / BOA PRÁTICA.
4. **Hierarquia e competência:** nunca presumir prevalência de norma federal, estadual ou municipal
   sem examinar a repartição constitucional (CF arts. 23, 24, 30, 225; LC 140/2011).
5. **Revisão adversarial obrigatória** (agente `revisor-juridico-adversarial`) antes de qualquer
   manifestação jurídica relevante (defesa, parecer, recurso, resposta a órgão, TAC/TC).
6. **Confiança e risco em toda conclusão relevante:** CONFIANÇA ALTA/MÉDIA/BAIXA e RISCO
   BAIXO/MODERADO/ELEVADO/MUITO ELEVADO.
7. **Proibidas respostas genéricas** ("consulte um advogado", "procure o órgão"). Investigue. Se há
   lacuna real, diga exatamente QUAL informação falta.
8. **Premissa técnica não se inventa.** Se a conclusão jurídica depende de conceito técnico
   (estágio sucessional, nascente, vazão, contaminação etc.), consulte o agente técnico competente
   ou registre a premissa como HIPÓTESE A CONFIRMAR. Ver `direito_ambiental/integracao/`.
9. **Data de corte:** toda análise informa a data das consultas e o nível de verificação das fontes.
10. **Não duplicar.** Antes de criar agente, ficha, índice, comando ou diretório, verificar se já
    existe (`direito_ambiental/indices/INDICE_GERAL.md`). Se existir, ATUALIZAR.
11. **Autocorreção rastreável.** Ao corrigir informação errada: corrigir a ficha, registrar em
    `direito_ambiental/CHANGELOG_JURIDICO_AMBIENTAL.md` (motivo + fonte), atualizar referências e
    checar contaminação em outros arquivos. Nunca apagar histórico silenciosamente.
12. **Toda pesquisa relevante vira memória**: registrar em `direito_ambiental/memoria/pesquisas/`
    usando o template, e indexar em `direito_ambiental/memoria/INDICE.md`.

### Formato padrão de resposta jurídica
QUESTÃO → RESPOSTA DIRETA (SIM / NÃO / DEPENDE / NÃO HÁ PREVISÃO EXPRESSA / HÁ CONTROVÉRSIA) →
FUNDAMENTO LEGAL → INTERPRETAÇÃO → JURISPRUDÊNCIA → APLICAÇÃO AO CASO → RISCO JURÍDICO →
ARGUMENTO CONTRÁRIO → CONCLUSÃO (+ CONFIANÇA + DATA DAS FONTES). Template:
`direito_ambiental/templates/RESPOSTA_JURIDICA.md`.

### Manutenção
- Após alterar fichas: `python3 direito_ambiental/scripts/gerar_indices.py` e
  `python3 direito_ambiental/scripts/validar_base.py`.
- Ambiente remoto: acesso HTTP direto a fontes oficiais pode estar bloqueado pela política de rede;
  `WebSearch` costuma funcionar. Registre o nível de verificação honestamente
  (`FONTE_PRIMARIA` / `INDIRETA` / `NAO_VERIFICADA`). Ver `direito_ambiental/fontes/CONTROLE_VIGENCIA.md`.

## Convenções gerais do repositório
- Idioma dos documentos: português (Brasil). Datas em ISO (AAAA-MM-DD) nos metadados.
- Não commitar dados pessoais de clientes nas fichas públicas; casos concretos ficam em
  `direito_ambiental/memoria/` com identificação mínima.
