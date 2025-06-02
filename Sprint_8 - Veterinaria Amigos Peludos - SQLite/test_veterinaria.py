import unittest
import os
import json
import csv

from clases import Mascota, Dueno, Consulta
from funciones import guardar_datos, pacientes, tutores

class TestVeterinaria(unittest.TestCase):

    def setUp(self):
        pacientes.clear()
        tutores.clear()
        self.dueno = Dueno("Carlos Perez", "3111234567", "Calle Falsa 123")
        self.mascota = Mascota("Firulais", "Perro", "Labrador", self.dueno)
        self.consulta = Consulta("20/05/2025", "Chequeo", "Saludable")

        self.csv_path = "test_mascotas.csv"
        self.json_path = "test_consultas.json"

    def tearDown(self):
        #Elimina archivos de prueba si existen
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        if os.path.exists(self.json_path):
            os.remove(self.json_path)

    def test_creacion_mascota(self):
        self.assertEqual(self.mascota.nombre_paciente, "Firulais")
        self.assertEqual(self.mascota.especie, "Perro")
        self.assertEqual(self.mascota.raza, "Labrador")
        self.assertEqual(self.mascota.dueno, self.dueno)

    def test_creacion_dueno(self):
        self.assertEqual(self.dueno.nombre_tutor, "Carlos Perez")
        self.assertEqual(self.dueno.telefono, "3111234567")
        self.assertEqual(self.dueno.direccion, "Calle Falsa 123")

    def test_creacion_consulta(self):
        self.assertEqual(self.consulta.fecha, "20/05/2025")
        self.assertEqual(self.consulta.motivo, "Chequeo")
        self.assertEqual(self.consulta.diagnostico, "Saludable")

    def test_excepcion_nombre_mascota_vacio(self):
        with self.assertRaises(ValueError):
            Mascota("", "Gato", "Siames", self.dueno)

    def test_excepcion_telefono_invalido(self):
        with self.assertRaises(ValueError):
            Dueno("Luis", "12345", "Calle 123")

    def test_serializacion_csv(self):
        pacientes.append(self.mascota)
        tutores.append(self.dueno)
        guardar_datos(csv_path=self.csv_path, json_path=self.json_path)

        self.assertTrue(os.path.exists(self.csv_path))

        with open(self.csv_path, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertGreater(len(rows), 0)
            self.assertEqual(rows[0]["nombre_mascota"], "Firulais")

    def test_serializacion_json(self):
        self.mascota.consultas.append(self.consulta)
        pacientes.append(self.mascota)
        guardar_datos(csv_path=self.csv_path, json_path=self.json_path)

        self.assertTrue(os.path.exists(self.json_path))

        with open(self.json_path, "r", encoding='utf-8') as f:
            data = json.load(f)
            self.assertIn("Firulais", data)
            self.assertEqual(data["Firulais"][0]["motivo"], "Chequeo")

if __name__ == '__main__':
    unittest.main()
