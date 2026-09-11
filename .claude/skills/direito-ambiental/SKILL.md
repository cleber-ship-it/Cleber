---
name: direito-ambiental
description: Consulta rápida de direito ambiental brasileiro (federal, RS, municipal) com acionamento automático dos agentes especializados do NUCLEO_DIREITO_AMBIENTAL, verificação de fontes, revisão adversarial e resposta no formato padrão. Use para qualquer dúvida jurídica ambiental (licenciamento, infração, APP, Mata Atlântica, supressão, outorga, responsabilidade, competência).
argument-hint: <pergunta jurídica ambiental, com município/UF e atividade quando possível>
---

# /direito-ambiental — consulta rápida

Questão: **$ARGUMENTS**

Execute o fluxo abaixo com rigor. Leia antes `CLAUDE.md` (regras 1-12), `direito_ambiental/PROTOCOLO_PESQUISA.md`
e `direito_ambiental/STATUS.md`. Data de hoje = data das fontes.

## 1. Triagem
Acione o agente `coordenador-direito-ambiental` em modo TRIAGEM com a questão. Se faltar município/UF ou
atividade e isso mudar materialmente a resposta, responda primeiro o que é comum (federal) e declare a
lacuna; NÃO bloqueie por perguntas triviais.

## 2. Memória como índice
Consulte `direito_ambiental/memoria/INDICE.md`, `direito_ambiental/indices/por_assunto.md` e o(s) arquivo(s)
de `direito_ambiental/temas/` indicados na triagem. Anote fichas relevantes e seus níveis/datas de verificação.
Se houver ficha `ALTERADA`, `EM_JULGAMENTO`, `EFICACIA_QUESTIONADA` ou verificação vencida (>180 dias) que
seja essencial, acione o `verificador-fontes-normativas` ANTES de concluir.

## 3. Especialistas (em paralelo, com a mesma triagem e perguntas específicas)
Acione, via Agent, os especialistas indicados na triagem — no mínimo `direito-ambiental-federal`; se RS,
`direito-ambiental-rs`; se houver município, `direito-ambiental-municipal`; mais os temáticos
(`licenciamento-ambiental`, `flora-app-mata-atlantica`, `infracoes-processo-administrativo`,
`responsabilidade-civil-ambiental`, `recursos-hidricos-saneamento`, `urbanistico-ambiental`) e
`jurisprudencia-ambiental` quando houver tese controvertida ou precedente necessário.

## 4. Verificação de fontes
Acione `verificador-fontes-normativas` com todas as `CITAÇÕES USADAS`. Citações NÃO CONFIRMADAS não
fundamentam a conclusão (podem aparecer como "hipótese a verificar").

## 5. Revisão adversarial
Monte a minuta consolidada e acione `revisor-juridico-adversarial`. Incorpore os ataques (RESOLVIDO / MANTIDO COMO RISCO).

## 6. Consolidação
Acione `coordenador-direito-ambiental` em modo CONSOLIDAÇÃO com: triagem, análises, verificação, revisão.
Entregue ao usuário a resposta no formato `direito_ambiental/templates/RESPOSTA_JURIDICA.md`
(QUESTÃO / RESPOSTA DIRETA / FUNDAMENTO LEGAL / INTERPRETAÇÃO / JURISPRUDÊNCIA / APLICAÇÃO AO CASO /
RISCO JURÍDICO / ARGUMENTO CONTRÁRIO / CONCLUSÃO + CONFIANÇA + DATA DAS FONTES + LACUNAS).

## 7. Memória e base
- Grave o bloco `MEMORIA` em `direito_ambiental/memoria/pesquisas/PESQ-<data>-<slug>.md` (template
  `PESQUISA_MEMORIA.md`) e adicione linha em `direito_ambiental/memoria/INDICE.md`.
- Para cada item de `FICHAS_A_CRIAR_OU_ATUALIZAR`: se já existe ficha, atualize; se não, crie a partir do
  template (nunca duplicar). Novidades/alterações → `CHANGELOG_JURIDICO_AMBIENTAL.md`.
- Rode `python3 direito_ambiental/scripts/gerar_indices.py && python3 direito_ambiental/scripts/validar_base.py`.

## Atalho para questões simples
Se a questão for trivial e integralmente respondida por ficha `FONTE_PRIMARIA`/`INDIRETA` recente, pode-se
pular as etapas 3 e 5, mas a resposta DEVE manter o formato padrão, a confiança, a data das fontes e a
advertência de que não houve revisão adversarial.
