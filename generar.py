"""Genera el informe HTML a partir del CSV validado."""

import argparse
import os
from datetime import UTC, datetime
from html import escape
from pathlib import Path

from analizar import analizar
from validar import COLUMNAS, CSV, RAIZ, cargar


def mostrar(valor):
    return "—" if valor is None else escape(str(valor))


def tabla(columnas, filas):
    cabecera = "".join(f'<th scope="col">{mostrar(c)}</th>' for c in columnas)
    cuerpo = "".join(
        "<tr>" + "".join(f"<td>{mostrar(fila[c])}</td>" for c in columnas) + "</tr>"
        for fila in filas
    )
    return f'<div class="tabla" tabindex="0"><table><thead><tr>{cabecera}</tr></thead><tbody>{cuerpo}</tbody></table></div>'


def generar(datos, autor, commit):
    indicadores = (
        ("Registros", datos["total"]), ("Caídas observadas · Fell", datos["fell"]),
        ("Hallazgos · Found", datos["found"]),
        ("Masa media (g)", round(datos["media"], 2) if datos["media"] is not None else None),
        ("Registros sin masa", datos["sin_masa"]),
    )
    tarjetas = "".join(f"<div><dt>{titulo}</dt><dd>{mostrar(valor)}</dd></div>" for titulo, valor in indicadores)
    maximo = datos["clases"][0][1]
    barras = "".join(
        f'<li><span>{mostrar(clase)}</span><meter aria-label="{mostrar(clase)}" min="0" max="{maximo}" value="{cantidad}"></meter><span>{cantidad}</span></li>'
        for clase, cantidad in datos["clases"]
    )
    fecha = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Meteoritos · Informe de datos</title>
<style>
* {{box-sizing:border-box}} body {{margin:0;background:#eef2f7;color:#182639;font:16px/1.55 system-ui,sans-serif}}
main {{max-width:1080px;margin:auto;padding:clamp(14px,4vw,42px)}} header,section {{padding:clamp(16px,3vw,32px);border-radius:14px;margin-bottom:18px}}
header {{background:#102b46;color:white}} h1 {{font-size:clamp(2rem,6vw,3.5rem);margin:.2em 0}}
header a {{color:#aee3ff}} code {{overflow-wrap:anywhere}} section {{background:white}} h2 {{margin-top:0}}
dl {{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:12px}}
dl div {{background:#f2f6fb;padding:12px;border-radius:8px}} dd {{font-size:1.5rem;font-weight:700;margin:0}}
ul {{padding:0;list-style:none}} li {{display:grid;grid-template-columns:minmax(65px,1fr) 3fr 56px;gap:8px;align-items:center;margin:.45em 0}}
meter {{width:100%;height:1.35em}} .tabla {{overflow:auto}} table {{border-collapse:collapse;width:100%;text-align:left}}
td,th {{padding:8px 12px;border-bottom:1px solid #dce4ee}} th {{background:#e7eef6}}
</style></head>
<body><main><header><p>INFORME DE DATOS · CI/CD</p><h1>Meteoritos</h1>
<p>Estudiante: {mostrar(autor)}</p>
<p>Fuente: The Meteoritical Society a través del <a href="https://data.nasa.gov/dataset/meteorite-landings">portal abierto de la NASA</a>.</p>
<p>Copia educativa. Las filas identificadas como simulaciones son ficticias.</p>
<p>Generado {fecha} · Commit <code>{mostrar(commit)}</code></p></header>
<section><h2>Indicadores</h2><dl>{tarjetas}</dl><p>La media usa solo masas disponibles e incluye los ceros.</p></section>
<section><h2>Diez clasificaciones más frecuentes</h2><ul>{barras}</ul></section>
<section><h2>Diez meteoritos de mayor masa</h2>{tabla(("name", "recclass", "mass (g)"), datos["mayores"])}</section>
<section><h2>Últimos diez registros del CSV</h2>{tabla(COLUMNAS, datos["ultimos"])}<p>El símbolo — indica un dato faltante.</p></section>
</main></body></html>
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=CSV)
    parser.add_argument("--salida", type=Path, default=RAIZ / "public" / "index.html")
    args = parser.parse_args()
    try:
        datos = analizar(cargar(args.csv))
        autor = (RAIZ / "estudiante.txt").read_text(encoding="utf-8-sig").strip()
        html = generar(datos, autor, os.getenv("GITHUB_SHA", "vista local"))
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(html, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Informe generado: {args.salida}")
