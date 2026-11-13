# DONKI-SEP — Pipeline de dados com a API aberta da NASA

Trabalho avaliativo do 3º trimestre (Grupo 6). Pipeline que coleta eventos de **partículas solares energéticas (SEP)** da API DONKI da NASA, grava em um banco PostgreSQL no Supabase e publica os dados em um painel web.

- **Painel:** https://sn-2026-grupo-06-nasa.github.io/DONKI-SEP/
- **Repositório:** https://github.com/SN-2026-GRUPO-06-NASA/DONKI-SEP
- **Organização:** SN-2026-GRUPO-06-NASA
- **Projeto Supabase:** DONKI-SEP-DB (região South America – São Paulo)

## Integrantes e divisão de responsabilidades

| Integrante | Responsabilidade |
|---|---|
| Brenno | Conversar com a IA: elaborar os prompts, obter as orientações e o código e esclarecer as dúvidas |
| Diogo | Aplicar as instruções: configurar GitHub, Supabase, Secrets, workflow e painel, executar o pipeline e testar os resultados |

## A API: DONKI / SEP

DONKI (*Space Weather Database Of Notifications, Knowledge, Information*) é o banco de dados de clima espacial da NASA. O endpoint **SEP** registra eventos de partículas solares energéticas: aumentos de partículas de alta energia (principalmente prótons) vindas do Sol, associados a erupções solares e ejeções de massa coronal. Esses eventos podem afetar satélites, comunicações e astronautas.

- Endpoint: `https://api.nasa.gov/DONKI/SEP?startDate=AAAA-MM-DD&endDate=AAAA-MM-DD&api_key=...`
- Autenticação: chave gratuita da NASA (`NASA_API_KEY`).
- Campos usados: `sepID` (chave natural), `eventTime`, `submissionTime`, `versionId`, `instruments`, `link`, `linkedEvents`.
- Particularidade: a API recusa intervalos de datas muito longos (erro 400), por isso o pipeline consulta em janelas de 30 dias.

## Arquitetura

```
NASA DONKI/SEP  →  GitHub Actions (scripts/fetch_nasa.py)  →  Supabase (PostgreSQL)  →  GitHub Pages (index.html)
```

1. **GitHub Actions** executa o workflow `update-data.yml` (agendado todo dia às 6h UTC e manualmente via `workflow_dispatch`).
2. **`scripts/fetch_nasa.py`** consulta a API, normaliza os campos, remove duplicados por `sep_id` (evita o erro PostgreSQL 21000) e envia os dados em lotes de 100 por upsert.
3. **Supabase** guarda os eventos em `sep_events` e o log de cada execução em `execucoes` (registros, lotes, erros e status: `concluido`, `erro_parcial`, `erro_critico`).
4. **`index.html`** (GitHub Pages) lê as duas tabelas pela API REST do Supabase e mostra tabela, contadores, filtros por ano e instrumento e a última atualização do pipeline.

### Modelagem e deduplicação

- Tabela `sep_events` com `UNIQUE (sep_id)`: o ID do evento é a chave natural, o que permite upsert sem duplicatas.
- A coluna `raw` (jsonb) guarda a resposta original da NASA.
- Em falha parcial, o script registra `erro_parcial` em `execucoes` e termina com `sys.exit(1)`, deixando o Actions vermelho.

### Segurança

- **RLS ativo** nas duas tabelas, com política de leitura pública.
- **GRANTs:** `SELECT` para `anon` e `authenticated`; `ALL` para `service_role`.
- `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` e `NASA_API_KEY` ficam como **Secrets** do GitHub, nunca no código.
- O `index.html` usa só a **publishable key** (somente leitura) e aplica `escapeHtml()` a todo valor externo inserido no HTML.
- O workflow usa `permissions: contents: read`, `concurrency` e `timeout-minutes`.

## Estrutura do repositório

```
DONKI-SEP/
├── index.html                      painel (GitHub Pages)
├── README.md
├── scripts/fetch_nasa.py           coleta, deduplicação e upsert
├── sql/setup.sql                   tabelas, constraint, RLS e GRANTs
├── .github/workflows/update-data.yml
└── docs/
    ├── tutorial.pdf
    ├── ai-interaction.md
    ├── reflexao.md
    └── apresentacao.pdf
```

## Como configurar (resumo)

O passo a passo completo está em `docs/tutorial.pdf`.

1. **NASA:** gerar a chave em api.nasa.gov.
2. **Supabase:** criar o projeto `DONKI-SEP-DB` e rodar `sql/setup.sql` no SQL Editor.
3. **GitHub Secrets** (Settings → Secrets and variables → Actions do repositório):
   - `SUPABASE_URL`: somente `https://SEU-PROJETO.supabase.co`, sem `/rest/v1`
   - `SUPABASE_SERVICE_KEY`: secret key (`service_role`)
   - `NASA_API_KEY`: chave da NASA
4. **Rodar o pipeline:** Actions → *Atualizar dados DONKI-SEP* → *Run workflow*.
5. **Painel:** no `index.html`, preencher `SUPABASE_URL` e `ANON_KEY` (publishable key) e ativar o GitHub Pages em Settings → Pages (branch `main`, pasta `/ (root)`).

## Uso de IA generativa

Utilizamos o **Claude (Anthropic)** como apoio na montagem do projeto: explicação da atividade, geração inicial do código e diagnóstico de erros a partir de logs e prints. Todos os prompts estão em [`docs/ai-interaction.md`](docs/ai-interaction.md) e a análise crítica em [`docs/reflexao.md`](docs/reflexao.md).

## Documentação

- [Tutorial](docs/tutorial.pdf)
- [Histórico de interações com IA](docs/ai-interaction.md)
- [Reflexão sobre o uso de IA](docs/reflexao.md)
- [Apresentação](docs/apresentacao.pdf)
