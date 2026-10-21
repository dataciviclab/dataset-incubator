"""Scarica da Eurostat domande e decisioni di protezione internazionale in Italia.

Produce un CSV tidy con una riga per (misura, anno, cittadinanza, dettaglio).
Le due fonti Eurostat (MIGR_ASYAPPCTZA, MIGR_ASYDCFSTA) hanno dimensioni diverse:
il preprocess le normalizza in un unico schema, necessario perche' il toolkit legge
un solo file raw.

Uso: python preprocess.py <anno> <output.csv>
L'anno e' ignorato: viene scaricata la serie completa (START_PERIOD -> ultimo anno).
"""

from __future__ import annotations

import csv
import re
import sys
import time
from itertools import chain
from pathlib import Path
from typing import Iterator
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1"
START_PERIOD = 2008
TIMEOUT_SECONDS = 120
MAX_TENTATIVI = 3
USER_AGENT = "dataciviclab-dataset-incubator/1.0"

FLUSSO_DECISIONI = "MIGR_ASYDCFSTA"
CHIAVE_DECISIONI = "A.PER..T.TOTAL..IT"
FLUSSO_DOMANDE = "MIGR_ASYAPPCTZA"
CHIAVE_DOMANDE = "A...T.PER.TOTAL.IT"
CODELIST_CITTADINANZE = "CITIZEN"

MIN_ANNI = 15
MIN_CITTADINANZE = 100

NUMERO = re.compile(r"^-?\d+(?:\.\d+)?$")
COLONNE = (
    "misura",
    "anno",
    "cittadinanza_codice",
    "cittadinanza",
    "dettaglio_codice",
    "valore",
)
Riga = tuple[str, str, str, str, str, int]


def _scarica(url: str) -> str:
    ultimo_errore: Exception | None = None
    for tentativo in range(1, MAX_TENTATIVI + 1):
        richiesta = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/tab-separated-values"})
        try:
            with urlopen(richiesta, timeout=TIMEOUT_SECONDS) as risposta:
                testo = risposta.read().decode("utf-8")
            break
        except HTTPError as errore:
            if 400 <= errore.code < 500 and errore.code != 429:
                raise RuntimeError(f"Richiesta non valida (HTTP {errore.code}): {url}") from errore
            ultimo_errore = errore
        except (URLError, TimeoutError) as errore:
            ultimo_errore = errore
        if tentativo < MAX_TENTATIVI:
            time.sleep(2 * tentativo)
    else:
        raise RuntimeError(f"Download fallito dopo {MAX_TENTATIVI} tentativi: {url} ({ultimo_errore})")

    if testo.lstrip().startswith("<"):
        raise RuntimeError(f"Risposta non TSV (probabile errore API): {testo[:200]}")
    return testo


def _leggi_tsv(testo: str) -> tuple[list[str], list[tuple[dict[str, str], dict[str, int | None]]]]:
    righe = testo.splitlines()
    if not righe:
        raise ValueError("Risposta TSV vuota")

    intestazione = righe[0].split("\t")
    dimensioni = [voce.split("\\")[0].strip() for voce in intestazione[0].split(",")]
    anni = [voce.strip() for voce in intestazione[1:]]
    if not anni or not all(re.fullmatch(r"\d{4}", anno) for anno in anni):
        raise ValueError(f"Intestazione TSV inattesa: {righe[0][:200]}")

    dati: list[tuple[dict[str, str], dict[str, int | None]]] = []
    for numero_riga, riga in enumerate(righe[1:], start=2):
        if not riga.strip():
            continue
        campi = riga.split("\t")
        valori_dimensione = campi[0].split(",")
        if len(valori_dimensione) != len(dimensioni):
            raise ValueError(
                f"Riga {numero_riga}: dimensioni attese {len(dimensioni)}, trovate {len(valori_dimensione)}"
            )
        valori_grezzi = campi[1:]
        if len(valori_grezzi) < len(anni):
            valori_grezzi += [""] * (len(anni) - len(valori_grezzi))
        elif len(valori_grezzi) > len(anni):
            raise ValueError(f"Riga {numero_riga}: anni attesi {len(anni)}, trovati {len(valori_grezzi)}")

        dimensioni_valori = dict(zip(dimensioni, valori_dimensione))
        valori: dict[str, int | None] = {}
        for anno, grezzo in zip(anni, valori_grezzi):
            testo_valore = grezzo.strip()
            valori[anno] = int(float(testo_valore)) if NUMERO.match(testo_valore) else None
        dati.append((dimensioni_valori, valori))
    return anni, dati


def _codelist(nome: str) -> dict[str, str]:
    testo = _scarica(f"{BASE_URL}/codelist/ESTAT/{nome}?format=TSV")
    etichette: dict[str, str] = {}
    for riga in testo.splitlines():
        if not riga.strip():
            continue
        codice, _, etichetta = riga.partition("\t")
        etichette[codice.strip()] = etichetta.strip()
    if not etichette:
        raise RuntimeError(f"Codelist {nome} vuota")
    return etichette


def _estrai(
    flusso: str,
    chiave: str,
    misura: str,
    dimensione_dettaglio: str,
    cittadinanze: dict[str, str],
) -> Iterator[Riga]:
    url = f"{BASE_URL}/data/{flusso}/{chiave}?format=TSV&startPeriod={START_PERIOD}"
    anni, dati = _leggi_tsv(_scarica(url))
    for dimensioni, valori in dati:
        cittadinanza_codice = dimensioni["citizen"].strip()
        dettaglio_codice = dimensioni[dimensione_dettaglio].strip()
        etichetta = cittadinanze.get(cittadinanza_codice, cittadinanza_codice)
        for anno in anni:
            valore = valori[anno]
            if valore is None:
                continue
            yield (misura, anno, cittadinanza_codice, etichetta, dettaglio_codice, valore)


def _valida(righe: dict[tuple[str, str, str, str], Riga]) -> None:
    anni = {riga[1] for riga in righe.values()}
    paesi = {riga[2] for riga in righe.values() if len(riga[2]) == 2}
    misure = {riga[0] for riga in righe.values()}
    if misure != {"domande", "decisioni"}:
        raise RuntimeError(f"Misure inattese: {sorted(misure)}")
    if len(anni) < MIN_ANNI:
        raise RuntimeError(f"Serie troppo corta: {len(anni)} anni (minimo {MIN_ANNI})")
    if len(paesi) < MIN_CITTADINANZE:
        raise RuntimeError(f"Poche cittadinanze: {len(paesi)} (minimo {MIN_CITTADINANZE})")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Uso: python preprocess.py <anno> <output.csv>", file=sys.stderr)
        return 2

    destinazione = Path(argv[2])
    cittadinanze = _codelist(CODELIST_CITTADINANZE)

    righe: dict[tuple[str, str, str, str], Riga] = {}
    estratte = chain(
        _estrai(FLUSSO_DECISIONI, CHIAVE_DECISIONI, "decisioni", "decision", cittadinanze),
        _estrai(FLUSSO_DOMANDE, CHIAVE_DOMANDE, "domande", "applicant", cittadinanze),
    )
    for riga in estratte:
        righe[(riga[0], riga[1], riga[2], riga[4])] = riga

    if not righe:
        print("Nessuna riga estratta da Eurostat", file=sys.stderr)
        return 1
    _valida(righe)

    destinazione.parent.mkdir(parents=True, exist_ok=True)
    temporaneo = destinazione.with_name(destinazione.name + ".tmp")
    with temporaneo.open("w", encoding="utf-8", newline="") as uscita:
        scrittore = csv.writer(uscita, lineterminator="\n")
        scrittore.writerow(COLONNE)
        scrittore.writerows(sorted(righe.values()))
    temporaneo.replace(destinazione)

    print(f"Scritte {len(righe)} righe in {destinazione}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
