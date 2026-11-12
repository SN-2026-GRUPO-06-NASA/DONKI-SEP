
# Histórico de Interação com IA

## Informações gerais

|Campo|Valor|
|-|-|
|**Grupo**|Grupo 6 (SN-2026-GRUPO-06-NASA)|
|**Integrantes**|Diogo, Brenno|
|**API NASA escolhida**|DONKI / SEP (Solar Energetic Particle)|
|**IA utilizada**|Claude (Anthropic)|
|**Data de início**|10-11-2026|
|**Data de conclusão**|12-11-2026|

---

## Interação 1 — Visão geral do trabalho e arquivos iniciais

**Data:** 10-11-2026
**Objetivo:** Entender o que a atividade exige e obter uma base prática para o pipeline.

**Prompt enviado à IA:**

```
o que eu preciso fazer neste trabalho me ensine de maneira pratica e me ajuda realiza lo
```
(anexos: PDF da atividade, print da planilha de grupos e o template ai-interaction.md)

**Resumo da resposta:**
Explicou o fluxo NASA → GitHub Actions → Supabase → GitHub Pages, listou os passos em ordem e gerou `sql/setup.sql`, `scripts/fetch_nasa.py`, `.github/workflows/update-data.yml` e `index.html`.

**O que funcionou:**
A estrutura geral, o `setup.sql` (rodou sem erro) e o `index.html`.

**O que precisou ajuste:**
O `fetch_nasa.py` pedia 365 dias de uma vez e a NASA recusou (ver Interação 10). O restante precisou de ajustes de configuração descritos nas interações seguintes.

---

## Interação 2 — Quais arquivos subir

**Data:** 10-11-2026
**Objetivo:** Saber exatamente quais arquivos enviar ao repositório e em quais pastas.

**Prompt enviado à IA:**

```
Suba os arquivos que gerei, mantendo a estrutura de pastas. - quais arquivos?
```

**Resumo da resposta:**
Listou os cinco arquivos gerados, a árvore de pastas esperada e duas formas de subir (site do GitHub ou Git).

**O que funcionou:**
A lista de arquivos e a árvore de pastas.

**O que precisou ajuste:**
A explicação não bastou para evitar o erro de caminho do workflow (Interação 9).

---

## Interação 3 — Dados do ai-interaction.md

**Data:** 10-11-2026
**Objetivo:** Preencher o template do histórico de IA.

**Prompt enviado à IA:**

```
mas o md falta por os dados certo?
```

**Resumo da resposta:**
Preencheu grupo, integrantes, API, IA e data de início, registrou as primeiras interações e deixou campos `[Preencher]` para o que dependia dos testes.

**O que funcionou:**
O preenchimento das informações gerais.

**O que precisou ajuste:**
As datas e os resultados reais foram revisados pelo grupo depois (esta versão do arquivo).

---

## Interação 5 — Rodar o setup.sql no Supabase

**Data:** 10-11-2026
**Objetivo:** Criar as tabelas, a constraint UNIQUE, o RLS e os GRANTs.

**Prompt enviado à IA:**

```
No SQL Editor, cole e rode o `sql/setup.sql`. Ele cria as duas tabelas, a constraint UNIQUE em `sep_id` (a chave natural dos eventos), o RLS com leitura pública e os GRANTs.
```
(trecho copiado da resposta anterior da IA, sem pergunta adicional)

**Resumo da resposta:**
Passo a passo do SQL Editor (New query → colar → Run), como conferir no Table Editor e o que cada parte do script faz.

**O que funcionou:**
O script rodou e criou `sep_events` e `execucoes`.

**O que precisou ajuste:**
Nenhum ajuste necessário.

---

## Interação 6 — Onde criar os Secrets

**Data:** 11-11-2026
**Objetivo:** Criar `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` e `NASA_API_KEY`.

**Prompt enviado à IA:**

```
onde e pra criar
```
(depois de colar o item "4. Secrets no GitHub" da resposta anterior da IA)

**Resumo da resposta:**
Indicou Settings do repositório → Secrets and variables → Actions → New repository secret e de onde copiar cada valor.

**O que funcionou:**
A localização do menu e a tabela de onde pegar cada valor.

**O que precisou ajuste:**
Primeiro foi aberto o menu de configurações da organização, e não do repositório (Interação 8).

---

## Interação 7 — Rodar o pipeline

**Data:** 11-11-2026
**Objetivo:** Executar o workflow manualmente.

**Prompt enviado à IA:**

```
(colou o item "5. Rodar o pipeline" da resposta anterior da IA, sem pergunta adicional)
```

**Resumo da resposta:**
Explicou Actions → Run workflow, como ler o log e uma tabela de erros comuns.

**O que funcionou:**
A tabela de erros comuns ajudou a interpretar os erros que apareceram depois.

**O que precisou ajuste:**
As primeiras execuções falharam (Interações 9, 10 e 11).

---

## Interação 8 — Tela errada ao procurar os Secrets

**Data:** 11-11-2026
**Objetivo:** Achar o menu de Secrets.

**Prompt enviado à IA:**

```
(print do menu Settings → Actions com General, Runners, Policies, Policy insights e OIDC; sem texto)
```

**Resumo da resposta:**
Identificou que era a configuração da organização e orientou a ir às configurações do repositório.

**O que funcionou:**
A IA reconheceu o menu pelas opções "Policies" e "OIDC", que só existem na organização.

**O que precisou ajuste:**
Nenhum.

---

## Interação 9 — Workflow não aparecia no Actions

**Data:** 11-11-2026
**Objetivo:** Fazer o Actions encontrar o `update-data.yml`.

**Prompts enviados à IA (em sequência):**

```
(print da aba Actions mostrando "Get started with GitHub Actions"; sem texto)
```
```
mas ja tem o update data la
```
```
(print do arquivo aberto, com o caminho scripts / .github / workflows / update-data.yml; sem texto)
```
```
(print da árvore de arquivos com .github/workflows dentro de scripts; sem texto)
```
```
ta e onde e pro fetch estar
```
```
ta agora oq devo fazer
```

**Resumo da resposta:**
A IA explicou que o Actions só lê `.github/workflows` na raiz do repositório e que o arquivo estava dentro de `scripts/`. Mandou recriar o arquivo no caminho certo, apagar o antigo e confirmou que `fetch_nasa.py` deveria continuar em `scripts/`.

**O que funcionou:**
Recriar o workflow na raiz fez o Actions listar "Atualizar dados DONKI-SEP".

**O que precisou ajuste:**
A primeira resposta da IA sugeriu criar o arquivo de novo sem notar que ele já existia; só depois do print do caminho a causa foi identificada.

---

## Interação 10 — Erro 400 da API da NASA

**Data:** 11-11-2026
**Objetivo:** Corrigir o erro do passo `python scripts/fetch_nasa.py`.

**Prompts enviados à IA:**

```
(print do log: ERRO: 400 Client Error: Bad Request for url: https://api.nasa.gov/DONKI/SEP?startDate=2025-11-11&endDate=2026-11-11&api_key=***; sem texto)
```
```
mande o codigo inteiro
```

**Resumo da resposta:**
A IA diagnosticou que a consulta de 365 dias era recusada e reescreveu `fetch()` para consultar em janelas de 30 dias, depois enviou o `fetch_nasa.py` completo.

**O que funcionou:**
Depois da correção a coleta passou a retornar 43 eventos únicos.

**O que precisou ajuste:**
Este foi um erro da IA: o script original assumia que a API aceitava 365 dias de uma vez, sem confirmar. A correção veio depois do erro real no Actions.

---

## Interação 11 — Erro 404 PGRST125 no Supabase

**Data:** 12-11-2026
**Objetivo:** Corrigir o erro ao enviar os dados ao Supabase.

**Prompts enviados à IA:**

```
(print do log: 43 eventos únicos / Lote falhou: 404 {"code":"PGRST125",...,"message":"Invalid path specified in request URL"}; sem texto)
```
```
isso?
```
(com print da tela Data API do Supabase mostrando a API URL terminando em /rest/v1/)

**Resumo da resposta:**
A IA apontou que o Secret `SUPABASE_URL` estava com `/rest/v1/` no final, o que duplicava o caminho, e orientou a usar só `https://...supabase.co`.

**O que funcionou:**
Depois de corrigir o Secret, a execução ficou verde (run #4) e os dados foram gravados.

**O que precisou ajuste:**
A IA primeiro levantou várias causas possíveis; o print da tela Data API confirmou qual era.

---

## Interação 12 — Diferença entre anon key e secret key

**Data:** 12-11-2026
**Objetivo:** Não expor a chave errada no `index.html`.

**Prompts enviados à IA:**

```
deu green
```
```
anon key é a secret key ne
```

**Resumo da resposta:**
A IA explicou que a publishable (anon) é pública e só lê, e a secret (service_role) ignora o RLS e fica só nos Secrets do GitHub. Também corrigiu uma informação própria: o prazo de entrega é 13/11, e não "hoje".

**O que funcionou:**
A tabela comparando as duas chaves; a chave colocada no `index.html` era a `sb_publishable_...`.

**O que precisou ajuste:**
Erro da IA: havia dito antes que a entrega era no mesmo dia da conversa.

---

## Interação 13 — Painel no GitHub Pages dando 404

**Data:** 12-11-2026
**Objetivo:** Publicar o painel.

**Prompts enviados à IA:**

```
(print de Settings → Pages já configurado em main / root; sem texto)
```
```
(colou o código completo do index.html com a URL e a publishable key)
```
```
ta dando erro 404
```
```
(print do Actions com 4 execuções do workflow e nenhuma "pages build and deployment"; sem texto)
```
```
dei commit e ta online agr
```

**Resumo da resposta:**
A IA validou a chave publishable, listou as causas possíveis do 404 e, pelo print, notou que não havia execução do Pages. Orientou a fazer um novo commit no `index.html` para forçar a publicação.

**O que funcionou:**
Depois do commit, o Pages publicou e o painel abriu.

**O que precisou ajuste:**
A primeira resposta tratou o 404 de forma genérica; só o print do Actions mostrou a causa.

---

## Interação 14 — Organizar as dificuldades para a entrega

**Data:** 12-11-2026
**Objetivo:** Reunir os problemas enfrentados e saber o que entra na entrega.

**Prompts enviados à IA:**

```
Crie uma planilha a partir da sua última resposta.
```
```
e se eu te mandar os prints e vc coletar todas as informaçoes das dificuldades que tive para montar o que devo entregar
```
```
Crie um Claude Doc a partir da sua última resposta.
```
```
posso adicionar isso para entrega?
```

**Resumo da resposta:**
A IA listou as seis dificuldades, criou um Claude Doc com elas (a planilha não chegou a ser gerada) e explicou que o doc não faz parte dos itens da seção 7.3 do PDF, devendo virar `ai-interaction.md` e `reflexao.md`.

**O que funcionou:**
A lista de dificuldades serviu de base para este arquivo e para a reflexão.

**O que precisou ajuste:**
A planilha foi pedida mas não entregue; o grupo não precisou dela.

---

## Interação 15 — Geração dos documentos finais

**Data:** 12-11-2026
**Objetivo:** Gerar `ai-interaction.md`, `reflexao.md` e o tutorial.

**Prompt enviado à IA:**

```
crie esses documentos, assim como o doc de tutorial
```

**Resumo da resposta:**
A IA gerou este arquivo, o `reflexao.md` e um tutorial em Claude Doc, exportável como PDF.

**O que funcionou:**
[Preencher após revisar.]

**O que precisou ajuste:**
[Preencher: o que o grupo corrigiu ou reescreveu nos documentos.]

---

## Resumo final

**Total de interações:** 15

**Principais contribuições da IA:**

* Explicou a arquitetura (Actions → Supabase → Pages) e gerou o código inicial do pipeline, do SQL e do painel.
* Interpretou logs e prints de erro e indicou a causa de cada falha.
* Explicou conceitos usados na arquitetura: RLS, GRANTs, upsert, deduplicação e diferença entre as chaves.

**Principais limitações encontradas:**

* O script inicial consultava 365 dias de uma vez e a API da NASA recusou (erro 400).
* Algumas respostas deram causas genéricas antes de ver o print do erro real.
* A IA errou o prazo de entrega em uma resposta.

**Avaliação geral do uso da IA:**
A IA acelerou a montagem do pipeline e ajudou a entender erros de configuração que travariam o grupo. Porém o código inicial tinha falhas que só apareceram ao rodar no Actions, e o grupo precisou testar, mandar prints e conferir cada passo. A IA funcionou melhor com o erro real em mãos do que com suposições.
