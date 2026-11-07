"""Extrae las primeras 20.000 filas de la descarga original de la NASA."""

import argparse
import csv
from itertools import islice
from pathlib import Path

COLUMNAS = ("id", "name", "recclass", "mass (g)", "fall", "year", "reclat", "reclong")
TOTAL = 20_000


def preparar(origen, destino):
    with origen.open(encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo, strict=True)
        cabecera = lector.fieldnames or []
        faltantes = set(COLUMNAS) - set(cabecera)
        if faltantes:
            raise ValueError(f"Faltan columnas: {', '.join(sorted(faltantes))}")
        if len(cabecera) != len(set(cabecera)):
            raise ValueError("Hay columnas duplicadas en la cabecera")
        muestra = []
        for fila in islice(lector, TOTAL):
            if None in fila or None in fila.values():
                raise ValueError(f"Linea {lector.line_num}: cantidad incorrecta de campos")
            muestra.append({columna: fila[columna] for columna in COLUMNAS})

    if len(muestra) != TOTAL:
        raise ValueError(f"Se esperaban al menos {TOTAL} registros, hay {len(muestra)}")

    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("x", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, COLUMNAS, lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(muestra)
    print(f"{len(muestra)} registros escritos en {destino}")
    for columna in ("mass (g)", "year", "reclat", "reclong"):
        vacios = sum(not fila[columna].strip() for fila in muestra)
        print(f"{columna}: {vacios} campos vacios")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origen", type=Path)
    args = parser.parse_args()
    try:
        preparar(args.origen, Path(__file__).resolve().parent / "datos" / "meteoritos.csv")
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Error: {error}\n")
