# Regras comuns a todos os agentes do NUCLEO_DIREITO_AMBIENTAL
(Cada agente do núcleo deve lê-lo no início da tarefa. Mantido fora de .claude/agents/ para não ser interpretado como agente.)

1. NÃO INVENTAR LEGISLAÇÃO OU JURISPRUDÊNCIA. Sem confirmação → "NÃO CONFIRMADO" e a citação não fundamenta conclusão.
2. MEMÓRIA ≠ VERDADE ATUAL. Fichas em `direito_ambiental/` são índice. Ler `verificacao.nivel`/`data_ultima_verificacao` e informar.
3. Toda citação: norma (nome, nº, art., §, inc., data, URL oficial, status, nível de verificação); julgado (tribunal, órgão, nº, relator, data, URL).
4. Separar TEXTO EXPRESSO / INTERPRETAÇÃO / JURISPRUDÊNCIA / PRÁTICA ADMINISTRATIVA / ENTENDIMENTO TÉCNICO; e OBRIGAÇÃO LEGAL / ENTENDIMENTO JURISPRUDENCIAL / EXIGÊNCIA ADMINISTRATIVA / BOA PRÁTICA.
5. Redação entre aspas SOMENTE se conferida na fonte; caso contrário, paráfrase marcada como tal.
6. Verificar vigência, alterações, competência (CF 23/24/30/225; LC 140/2011), exceções, jurisprudência, tese contrária.
7. Toda conclusão relevante: CONFIANÇA (ALTA/MÉDIA/BAIXA) + RISCO (BAIXO/MODERADO/ELEVADO/MUITO ELEVADO) + DATA DAS FONTES + nível de verificação.
8. Proibido genérico ("consulte um advogado", "procure o órgão"). Se há lacuna, dizer QUAL informação falta.
9. Premissa técnica não se inventa: marcar como HIPÓTESE A CONFIRMAR e indicar o agente técnico (ver `direito_ambiental/integracao/PROTOCOLO_INTEGRACAO.md`).
10. Ser crítico: se a tese do usuário é fraca, dizer.
11. Ao usar WebSearch/WebFetch, preferir fontes oficiais (`direito_ambiental/fontes/FONTES_OFICIAIS.md`). Se o acesso direto estiver bloqueado (situação constatada neste ambiente remoto em 2026-09-11 — ver STATUS.md), registrar nível INDIRETA e dizer isso na resposta; FONTE_PRIMARIA só com leitura efetiva do texto oficial ou documento fornecido pelo usuário.
12. Antes de propor criação de ficha/arquivo, verificar se já existe (`direito_ambiental/indices/`). Se existir, propor atualização.
13. Saída: começar SEMPRE com um bloco `CITAÇÕES USADAS` (dispensado apenas no modo TRIAGEM do coordenador e na saída do verificador, que tem formato próprio) (lista de IDs/normas/julgados com nível de verificação) para o verificador e o revisor.
