
-- DONKI-SEP-DB: rode no Supabase (SQL Editor)
create table if not exists public.sep_events (
  id bigserial primary key,
  sep_id text not null,
  event_time timestamptz not null,
  submission_time timestamptz,
  version_id int,
  instruments text[],
  link text,
  linked_events jsonb,
  raw jsonb,
  inserted_at timestamptz default now(),
  constraint uq_sep_events_sep_id unique (sep_id)  -- chave natural (permite upsert)
);

create table if not exists public.execucoes (
  id bigserial primary key,
  executado_em timestamptz default now(),
  registros_processados int default 0,
  lotes int default 0,
  erros int default 0,
  status text check (status in ('concluido','erro_parcial','erro_critico')),
  mensagem text
);

alter table public.sep_events enable row level security;
alter table public.execucoes  enable row level security;

create policy "leitura publica sep_events" on public.sep_events for select using (true);
create policy "leitura publica execucoes"  on public.execucoes  for select using (true);

grant usage on schema public to anon, authenticated, service_role;
grant select on public.sep_events, public.execucoes to anon, authenticated;
grant all on public.sep_events, public.execucoes to service_role;
grant usage, select on all sequences in schema public to service_role;
