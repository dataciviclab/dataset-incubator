#!/usr/bin/env python3
"""Scarica XLSX da TERNA e rimuove la riga di footer 'Applied filters'.

Uso:
  python fetch_terna.py <year> <output.xlsx>

Esempio:
  python fetch_terna.py 2015 output.xlsx
"""

import sys
import zipfile
import shutil
import tempfile
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

URL_TEMPLATE = (
    "https://dati.terna.it/api/sitecore/dati/downloadcenter/records"
    "?f=xlsx&filterDataset=ElectricalEnergy&filterYear={year}"
    "&filterMonth=12&orderByColumn=Anno&orderByDir=desc&db=dati&pageSize=500000"
)


def strip_footer(input_path: Path, output_path: Path) -> None:
    """Rimuove la riga 'Applied filters:' dal XLSX."""
    ET.register_namespace("", "http://schemas.openxmlformats.org/spreadsheetml/2006/main")
    ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

    with tempfile.TemporaryDirectory() as tmp:
        tmp_xlsx = Path(tmp) / "out.xlsx"
        with zipfile.ZipFile(input_path) as zin:
            with zipfile.ZipFile(tmp_xlsx, "w") as zout:
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename == "xl/worksheets/sheet1.xml":
                        root = ET.fromstring(data)
                        sheet_data = root.find(".//s:sheetData", ns)
                        if sheet_data is not None:
                            for row in list(sheet_data.findall("s:row", ns)):
                                first_cell = row.find("s:c", ns)
                                if first_cell is not None:
                                    val = None
                                    for tag in ["s:is/s:t", "s:v"]:
                                        el = first_cell.find(tag, ns)
                                        if el is not None and el.text:
                                            val = el.text
                                            break
                                    if val and "Applied filters" in str(val):
                                        sheet_data.remove(row)
                        data = ET.tostring(root, xml_declaration=True, encoding="UTF-8")
                    zout.writestr(item, data)
        shutil.copy(tmp_xlsx, output_path)


if __name__ == "__main__":
    year = sys.argv[1]
    output = Path(sys.argv[2])
    url = URL_TEMPLATE.format(year=year)

    print(f"Downloading {url}...")
    tmp_raw = Path(tempfile.mktemp(suffix=".xlsx"))
    urllib.request.urlretrieve(url, tmp_raw)

    print("Stripping footer...")
    strip_footer(tmp_raw, output)
    tmp_raw.unlink()

    size = output.stat().st_size
    print(f"Saved {output.name} ({size / 1024:.0f} KB)")
