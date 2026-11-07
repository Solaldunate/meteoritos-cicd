import csv
import tempfile
import unittest
from pathlib import Path

from analizar import analizar
from validar import COLUMNAS, cargar

VALIDO = (100, "Simulacion A", "H5", "20", "Found", "2026", "0", "-65")


class PruebasMeteoritos(unittest.TestCase):
    def leer(self, *filas, cabecera=COLUMNAS):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "prueba.csv"
            with ruta.open("w", encoding="utf-8", newline="") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(cabecera)
                escritor.writerows(filas)
            return cargar(ruta)

    def test_registro_valido(self):
        fila, = self.leer(VALIDO)
        self.assertEqual((fila["id"], fila["year"], fila["reclat"]), (100, 2026, 0))

    def test_media_conocida(self):
        otro = (101, "Simulacion B", "L5", "40", "Fell", "", "", "")
        datos = analizar(self.leer(VALIDO, otro))
        self.assertEqual((datos["media"], datos["fell"], datos["found"]), (30, 1, 1))
        self.assertEqual(datos["mayores"][0]["id"], 101)

    def test_faltantes_y_cero(self):
        sin_masa = (101, "Simulacion B", "L5", "", "Fell", "", "", "")
        masa_cero = (102, "Simulacion C", "H5", "0", "Found", "", "", "")
        filas = self.leer(VALIDO, sin_masa, masa_cero)
        self.assertIsNone(filas[1]["mass (g)"])
        self.assertIsNone(filas[1]["year"])
        self.assertIsNone(filas[1]["reclat"])
        self.assertEqual(analizar(filas)["sin_masa"], 1)
        self.assertEqual(analizar(filas)["media"], 10)

    def test_masa_negativa(self):
        with self.assertRaisesRegex(ValueError, r"Fila 2.*mass \(g\)"):
            self.leer((*VALIDO[:3], "-1", *VALIDO[4:]))

    def test_coordenadas_fuera_de_rango(self):
        with self.assertRaisesRegex(ValueError, r"Fila 2.*reclat[\s\S]*Fila 2.*reclong"):
            self.leer((*VALIDO[:6], "91", "-181"))

    def test_identificador_duplicado(self):
        with self.assertRaisesRegex(ValueError, r"Fila 3.*id.*duplicado"):
            self.leer(VALIDO, ("0100", *VALIDO[1:]))

    def test_fecha_completa(self):
        for texto in ("1880-01-01", "1880-01-01T00:00:00", "01/01/1880 12:00:00 AM"):
            with self.subTest(texto=texto):
                fila, = self.leer((*VALIDO[:5], texto, *VALIDO[6:]))
                self.assertEqual(fila["year"], 1880)

    def test_masa_no_finita(self):
        for texto in ("NaN", "Infinity"):
            with self.subTest(texto=texto):
                with self.assertRaisesRegex(ValueError, "finito"):
                    self.leer((*VALIDO[:3], texto, *VALIDO[4:]))

    def test_cabecera_incompleta(self):
        with self.assertRaisesRegex(ValueError, "Fila 1.*reclong"):
            self.leer(cabecera=COLUMNAS[:-1])

    def test_fila_incompleta(self):
        with self.assertRaisesRegex(ValueError, "Fila 2.*estructura"):
            self.leer(VALIDO[:-1])


if __name__ == "__main__":
    unittest.main()
