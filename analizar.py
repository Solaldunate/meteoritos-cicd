"""Calcula los indicadores del informe a partir de registros validados."""

from collections import Counter


def analizar(registros):
    con_masa = [fila for fila in registros if fila["mass (g)"] is not None]
    tipos = Counter(fila["fall"] for fila in registros)
    clases = Counter(fila["recclass"] for fila in registros)
    media = (
        sum(fila["mass (g)"] for fila in con_masa) / len(con_masa)
        if con_masa else None
    )
    return {
        "total": len(registros),
        "fell": tipos["Fell"],
        "found": tipos["Found"],
        "media": media,
        "sin_masa": len(registros) - len(con_masa),
        "clases": clases.most_common(10),
        "mayores": sorted(con_masa, key=lambda fila: fila["mass (g)"], reverse=True)[:10],
        "ultimos": registros[-10:],
    }
