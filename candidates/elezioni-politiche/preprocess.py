#!/usr/bin/env python3
"""Scarica, estrae e unifica risultati elezioni politiche (Camera+Senato 1948-2022)."""

import csv
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent / "cache"
HEADER = [
    "data_elezione",
    "camera_senato",
    "circoscrizione",
    "provincia",
    "comune",
    "collegio_plurinominale",
    "collegio_uninominale",
    "elettori_totali",
    "elettori_maschi",
    "votanti_totali",
    "votanti_maschi",
    "schede_biache",
    "lista",
    "voti_lista",
    "descr_lista",
    "cognome",
    "nome",
    "luogo_nascita",
    "data_nascita",
    "sesso",
    "voti_candidato",
]

ELECTIONS = [
    (1948, "18-04", "19480418"),
    (1953, "07-06", "19530607"),
    (1958, "25-05", "19580525"),
    (1963, "28-04", "19630428"),
    (1968, "19-05", "19680519"),
    (1972, "07-05", "19720507"),
    (1976, "20-06", "19760620"),
    (1979, "03-06", "19790603"),
    (1983, "26-06", "19830626"),
    (1987, "14-06", "19870614"),
    (1992, "05-04", "19920405"),
    (1994, "27-03", "19940327"),
    (1996, "21-04", "19960421"),
    (2001, "13-05", "20010513"),
    (2006, "09-04", "20060409"),
    (2008, "13-04", "20080413"),
    (2013, "24-02", "20130224"),
    (2018, "04-03", "20180304"),
    (2022, "25-09", "20220925"),
]


def _int(val):
    if val and val.replace("-", "").strip().isdigit():
        return int(val)
    return None


def _dload(url, dest):
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    curl = shutil.which("curl")
    if curl:
        subprocess.run(
            [curl, "-k", "-sS", "-L", "--max-time", "120", "-o", str(dest), url],
            check=True,
            timeout=120,
        )
        return
    import ssl
    import urllib.request

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
        dest.write_bytes(r.read())


def _extract(zip_path, out_dir):
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.lower().endswith((".csv", ".txt")):
                d = out_dir / Path(name).name
                if not d.exists():
                    z.extract(name, out_dir)


def _rows(fp, row_fn, de, delim=";", encoding="utf-8"):
    if not fp.exists():
        # fallback case-insensitive (es. Camera- vs camera- nel 1987)
        parent = fp.parent
        if parent.is_dir():
            for child in parent.iterdir():
                if child.name.lower() == fp.name.lower():
                    fp = child
                    break
        if not fp.exists():
            return []
    out = []
    with open(fp, encoding=encoding, errors="replace") as f:
        for r in csv.DictReader(f, delimiter=delim):
            r = {k.strip(): v.strip() if v else None for k, v in r.items()}
            rec = row_fn(r, de)
            if rec.get("lista") or rec.get("voti_lista") is not None:
                out.append(rec)
    return out


def _base(de, cs):
    return {
        "data_elezione": de,
        "camera_senato": cs,
        "circoscrizione": None,
        "provincia": None,
        "comune": None,
        "collegio_plurinominale": None,
        "collegio_uninominale": None,
        "elettori_totali": None,
        "elettori_maschi": None,
        "votanti_totali": None,
        "votanti_maschi": None,
        "schede_biache": None,
        "lista": None,
        "voti_lista": None,
        "descr_lista": None,
        "cognome": None,
        "nome": None,
        "luogo_nascita": None,
        "data_nascita": None,
        "sesso": None,
        "voti_candidato": None,
    }


def r_cam_ep1(row, de):
    r = _base(de, "C")
    r.update(
        circoscrizione=row["CIRCOSCRIZIONE"],
        provincia=row["PROVINCIA"],
        comune=row["COMUNE"],
        elettori_totali=_int(row["ELETTORI"]),
        elettori_maschi=_int(row["ELETTORI_MASCHI"]),
        votanti_totali=_int(row["VOTANTI"]),
        votanti_maschi=_int(row["VOTANTI_MASCHI"]),
        schede_biache=_int(row["SCHEDE_BIANCHE"]),
        lista=row["LISTA"],
        voti_lista=_int(row["VOTI_LISTA"]),
    )
    return r


def r_cam_porc(row, de):
    r = _base(de, "C")
    r.update(
        circoscrizione=row["CIRCOSCRIZIONE"],
        provincia=row["PROVINCIA"],
        comune=row["COMUNE"],
        elettori_totali=_int(row["ELETTORI"]),
        elettori_maschi=_int(row["ELETTORI_MASCHI"]),
        votanti_totali=_int(row["VOTANTI"]),
        votanti_maschi=_int(row["VOTANTI_MASCHI"]),
        schede_biache=_int(row["SCHEDE_BIANCHE"]),
        lista=row["LISTA"],
        voti_lista=_int(row.get("VOTI_LISTA") or row.get("VOTILISTA")),
    )
    return r


def r_sen_ep1(row, de):
    r = _base(de, "S")
    r.update(
        circoscrizione=row["REGIONE"],
        comune=row["COMUNE"],
        collegio_plurinominale=row["COLLEGIO"],
        elettori_totali=_int(row["ELETTORI"]),
        elettori_maschi=_int(row["ELETTORI_MASCHI"]),
        votanti_totali=_int(row["VOTANTI"]),
        votanti_maschi=_int(row["VOTANTI_MASCHI"]),
        schede_biache=_int(row["SCHEDE_BIANCHE"]),
        lista=row["LISTA"],
        voti_lista=_int(row["VOTI_LISTA"]),
    )
    return r


def r_sen_porc(row, de):
    r = _base(de, "S")
    r.update(
        circoscrizione=row["REGIONE"],
        provincia=row["PROVINCIA"],
        comune=row["COMUNE"],
        elettori_totali=_int(row.get("ELETTORI_TOTALI") or row.get("ELETTORI")),
        elettori_maschi=_int(row["ELETTORI_MASCHI"]),
        votanti_totali=_int(row.get("VOTANTI_TOTALI") or row.get("VOTANTI")),
        votanti_maschi=_int(row["VOTANTI_MASCHI"]),
        schede_biache=_int(row["SCHEDE_BIANCHE"]),
        lista=row["LISTA"],
        voti_lista=_int(row["VOTI_LISTA"]),
    )
    return r


def r_matt_prop(row, de):
    r = _base(de, "C")
    r.update(
        circoscrizione=row["CIRCOSCRIZIONE"],
        comune=row["COMUNE"],
        collegio_plurinominale=row["COLLEGIO"],
        elettori_totali=_int(row["ELETTORI"]),
        elettori_maschi=_int(row["ELETTORI_MASCHI"]),
        votanti_totali=_int(row["VOTANTI"]),
        votanti_maschi=_int(row["VOTANTI_MASCHI"]),
        schede_biache=_int(row["SCHEDE_BIANCHE"]),
        lista=row["LISTA"],
        voti_lista=_int(row["VOTI_LISTA"]),
    )
    return r


def r_matt_uni(row, de):
    r = _base(de, "C")
    r.update(
        circoscrizione=row["circ"],
        comune=row["comune"],
        collegio_plurinominale=row["coll"],
        lista=row["descrcontrass"],
        voti_lista=_int(row["TOTVOTI"]),
        descr_lista=row["descrcontrass"],
        cognome=row["cognome"],
        nome=row["nome"],
        luogo_nascita=row["luogonascita"],
        data_nascita=row["datanascita"],
        sesso=row["sesso"],
        voti_candidato=_int(row["TOTVOTI"]),
    )
    return r


def r_sen_matt(row, de):
    r = _base(de, "S")
    r.update(
        circoscrizione=row["REGIONE"],
        comune=row["COMUNE"],
        collegio_plurinominale=row["COLLEGIO"],
        elettori_totali=_int(row["ELETTORI"]),
        elettori_maschi=_int(row["ELETTORI_MASCHI"]),
        votanti_totali=_int(row["VOTANTI"]),
        votanti_maschi=_int(row["VOTANTI_MASCHI"]),
        schede_biache=_int(row["SCHEDE_BIANCHE"]),
        lista=row["LISTA"],
        voti_lista=_int(row["VOTI_LISTA"]),
    )
    return r


def r_ros18(row, de, cs):
    r = _base(de, cs)
    r.update(
        circoscrizione=row.get("CIRCOSCRIZIONE") or row.get("REGIONE"),
        comune=row["COMUNE"],
        collegio_plurinominale=row["COLLEGIOPLURINOMINALE"],
        collegio_uninominale=row["COLLEGIOUNINOMINALE"],
        elettori_totali=_int(row["ELETTORI"]),
        elettori_maschi=_int(row["ELETTORI_MASCHI"]),
        votanti_totali=_int(row["VOTANTI"]),
        votanti_maschi=_int(row["VOTANTI_MASCHI"]),
        schede_biache=_int(row["SCHEDE_BIANCHE"]),
        lista=row["LISTA"],
        voti_lista=_int(row["VOTI_LISTA"]),
        cognome=row["COGNOME"],
        nome=row["NOME"],
        luogo_nascita=row["LUOGO_NASCITA"],
        data_nascita=row["DATA_NASCITA"],
        sesso=row["SESSO"],
        voti_candidato=_int(row["VOTI_CANDIDATO"]),
    )
    return r


def r_ros22(row, de, cs):
    r = _base(de, cs)
    r.update(
        circoscrizione=row["CIRC-REG"],
        comune=row["COMUNE"],
        collegio_plurinominale=row["COLLPLURI"],
        collegio_uninominale=row["COLLUNINOM"],
        elettori_totali=_int(row["ELETTORITOT"]),
        elettori_maschi=_int(row["ELETTORIM"]),
        votanti_totali=_int(row["VOTANTITOT"]),
        votanti_maschi=_int(row["VOTANTIM"]),
        schede_biache=_int(row["SKBIANCHE"]),
        lista=row["DESCRLISTA"],
        voti_lista=_int(row["VOTILISTA"]),
        descr_lista=row["DESCRLISTA"],
        cognome=row["COGNOME"],
        nome=row["NOME"],
        luogo_nascita=row["LUOGONASCITA"],
        data_nascita=row["DATANASCITA"],
        sesso=row["SESSO"],
        voti_candidato=_int(row["VOTICANDIDATO"]),
    )
    return r


def main():
    if len(sys.argv) < 3:
        print("Uso: python preprocess.py <year> <output.csv>", file=sys.stderr)
        sys.exit(1)
    output_path = Path(sys.argv[2])
    tmp = CACHE_DIR / "extracted"
    tmp.mkdir(parents=True, exist_ok=True)
    all_rows = []

    for anno, date_str, ymd in ELECTIONS:
        cz = CACHE_DIR / f"cam-{ymd}.zip"
        _dload(f"https://dait.interno.gov.it/documenti/opendata/camera/camera-{ymd}.zip", cz)
        cd = tmp / "cam" / ymd
        cd.mkdir(parents=True, exist_ok=True)
        _extract(cz, cd)
        sz = CACHE_DIR / f"sen-{ymd}.zip"
        _dload(f"https://dait.interno.gov.it/documenti/opendata/senato/senato-{ymd}.zip", sz)
        sd = tmp / "sen" / ymd
        sd.mkdir(parents=True, exist_ok=True)
        _extract(sz, sd)

        dd, mm = date_str.split("-")
        de = f"{anno}-{mm}-{dd}"
        rows = []

        if anno <= 1992:
            rows += _rows(cd / f"camera-{ymd}.txt", r_cam_ep1, de)
            rows += _rows(sd / f"senato-{ymd}.txt", r_sen_ep1, de)
        elif anno <= 2001:
            rows += _rows(cd / f"camera-{ymd}_Proporzionale.txt", r_matt_prop, de)
            rows += _rows(cd / f"Camera_{ymd}_Uninom_Cand&Contr.txt", r_matt_uni, de)
            rows += _rows(sd / f"senato-{ymd}.txt", r_sen_matt, de)
        elif anno <= 2013:
            rows += _rows(cd / f"camera_italia-{ymd}.txt", r_cam_porc, de)
            rows += _rows(sd / f"senato_italia-{ymd}.txt", r_sen_porc, de)
        elif anno == 2018:
            rows += _rows(cd / "Camera2018_livComune.txt", lambda r, d: r_ros18(r, d, "C"), de)
            rows += _rows(sd / "Senato2018_livComune.txt", lambda r, d: r_ros18(r, d, "S"), de)
        elif anno == 2022:
            rows += _rows(
                cd / "camera2022_Italia_LivComune.csv",
                lambda r, d: r_ros22(r, d, "C"),
                de,
                delim=";",
            )
            rows += _rows(
                sd / "Senato_Italia_LivComune.csv", lambda r, d: r_ros22(r, d, "S"), de, delim=";"
            )

        all_rows += rows
        print(f"  {anno}: {len(rows)} righe", flush=True)

    if not all_rows:
        print("ERRORE: nessun dato estratto", file=sys.stderr)
        sys.exit(1)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(all_rows)
    print(f"\nFatto: {len(all_rows)} righe scritte in {output_path}", flush=True)


if __name__ == "__main__":
    main()
