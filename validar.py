"""Validacion del CSV y conversion de sus campos a tipos de Python."""

import argparse
import csv
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CSV = RAIZ / "datos" / "meteoritos.csv"
COLUMNAS = ("id", "name", "recclass", "mass (g)", "fall", "year", "reclat", "reclong")


def numero(texto, minimo, maximo=None):
    if not texto:
        return None
    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError("se requiere un numero") from None
    if not valor.is_finite() or valor < minimo or (maximo is not None and valor > maximo):
        limite = f"entre {minimo} y {maximo}" if maximo is not None else f"mayor o igual a {minimo}"
        raise ValueError(f"se requiere un numero finito {limite}")
    return valor


def anio(texto):
    if not texto:
        return None
    if re.fullmatch(r"[0-9]{1,4}", texto):
        valor = int(texto)
    else:
        for formato in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y %I:%M:%S %p"):
            try:
                valor = datetime.strptime(texto, formato).year
                break
            except ValueError:
                pass
        else:
            raise ValueError("se requiere un anio entero o una fecha valida") from None
    if not 1 <= valor <= 2026:
        raise ValueError("el anio debe estar entre 1 y 2026")
    return valor


def cargar(ruta=CSV):
    registros = []
    ids = {}
    errores = []
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        lector = csv.reader(archivo, strict=True)
        try:
            cabecera = next(lector, [])
            faltan = [campo for campo in COLUMNAS if campo not in cabecera]
            if faltan:
                raise ValueError(f"Fila 1 | cabecera | faltan columnas: {', '.join(faltan)}")
            if len(cabecera) != len(set(cabecera)):
                raise ValueError("Fila 1 | cabecera | columnas repetidas")
            while True:
                linea = lector.line_num + 1
                valores = next(lector, None)
                if valores is None:
                    break
                if len(valores) != len(cabecera):
                    errores.append(f"Fila {linea} | estructura | se esperaban {len(cabecera)} campos, llegaron {len(valores)}")
                    continue
                fila = dict(zip(cabecera, (valor.strip() for valor in valores)))
                inicio = len(errores)

                def error(campo, motivo):
                    errores.append(f"Fila {linea} | {campo} | {motivo} (valor {fila[campo]!r})")

                identificador = fila["id"]
                try:
                    if not re.fullmatch(r"[0-9]+", identificador) or int(identificador) < 1:
                        raise ValueError
                    identificador = int(identificador)
                except ValueError:
                    error("id", "se requiere un entero positivo")
                else:
                    if identificador in ids:
                        error("id", f"identificador duplicado, ya aparece en fila {ids[identificador]}")
                    else:
                        ids[identificador] = linea
                for campo in ("name", "recclass"):
                    if not fila[campo]:
                        error(campo, "texto obligatorio")
                if fila["fall"] not in ("Fell", "Found"):
                    error("fall", "se requiere Fell o Found")

                convertido = {campo: fila[campo] for campo in COLUMNAS}
                convertido["id"] = identificador
                for campo, minimo, maximo in (
                    ("mass (g)", 0, None), ("reclat", -90, 90), ("reclong", -180, 180)
                ):
                    try:
                        convertido[campo] = numero(fila[campo], minimo, maximo)
                    except ValueError as fallo:
                        error(campo, str(fallo))
                try:
                    convertido["year"] = anio(fila["year"])
                except ValueError as fallo:
                    error("year", str(fallo))
                if len(errores) == inicio:
                    registros.append(convertido)
        except csv.Error as fallo:
            errores.append(f"Fila {lector.line_num or 1} | estructura | {fallo}")
    if errores:
        raise ValueError("\n".join(errores))
    if not registros:
        raise ValueError("Fila 2 | estructura | se requiere al menos un registro")
    return registros


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, default=CSV)
    args = parser.parse_args()
    try:
        registros = cargar(args.csv)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Validacion correcta: {len(registros):,} registros.")
