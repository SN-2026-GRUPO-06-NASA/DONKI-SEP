import os, sys, requests
from datetime import date, timedelta

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
NASA_KEY = os.environ.get("NASA_API_KEY", "DEMO_KEY")
DAYS = int(os.environ.get("DAYS", "365"))
BATCH = 100

HDR = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}",
       "Content-Type": "application/json"}

def log_execucao(proc, lotes, erros, status, msg=""):
    requests.post(f"{SUPABASE_URL}/rest/v1/execucoes", headers={**HDR, "Prefer": "return=minimal"},
        json={"registros_processados": proc, "lotes": lotes, "erros": erros,
              "status": status, "mensagem": msg[:500]}, timeout=30)

def fetch():
    fim = date.today()
    ini = fim - timedelta(days=DAYS)
    eventos = []
    atual = ini
    while atual < fim:
        fim_janela = min(atual + timedelta(days=29), fim)
        r = requests.get("https://api.nasa.gov/DONKI/SEP",
            params={"startDate": atual.isoformat(), "endDate": fim_janela.isoformat(),
                    "api_key": NASA_KEY}, timeout=60)
        if not r.ok:
            raise RuntimeError(f"{r.status_code}: {r.text[:300]}")
        eventos.extend(r.json() or [])
        atual = fim_janela + timedelta(days=1)
    return eventos

def normalize(e):
    return {
        "sep_id": e.get("sepID"),
        "event_time": e.get("eventTime"),
        "submission_time": e.get("submissionTime"),
        "version_id": e.get("versionId"),
        "instruments": [i.get("displayName") for i in (e.get("instruments") or [])],
        "link": e.get("link"),
        "linked_events": e.get("linkedEvents"),
        "raw": e,
    }

def main():
    try:
        rows = [normalize(e) for e in fetch()]
    except Exception as ex:
        log_execucao(0, 0, 1, "erro_critico", str(ex)); print("ERRO:", ex); sys.exit(1)

    unicos = {r["sep_id"]: r for r in rows if r["sep_id"]}  # dedup (evita erro 21000)
    rows = list(unicos.values())
    print(f"{len(rows)} eventos únicos")

    lotes = erros = enviados = 0
    for i in range(0, len(rows), BATCH):
        lote = rows[i:i+BATCH]
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/sep_events?on_conflict=sep_id",
            headers={**HDR, "Prefer": "resolution=merge-duplicates,return=minimal"},
            json=lote, timeout=60)
        lotes += 1
        if resp.ok: enviados += len(lote)
        else: erros += 1; print("Lote falhou:", resp.status_code, resp.text)

    status = "concluido" if erros == 0 else "erro_parcial"
    log_execucao(enviados, lotes, erros, status)
    if erros: sys.exit(1)

if __name__ == "__main__":
    main()
