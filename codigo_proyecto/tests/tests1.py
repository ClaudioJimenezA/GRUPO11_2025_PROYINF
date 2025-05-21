import unittest
import sys
from django.test import Client
from editor.models import Boletin


class TestEditarBoletin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        print("\n=== Pruebas de edición de boletines existentes e inexistentes ===")
        print("-> Creando boletín de prueba...")
        response = cls.client.post('/editor/nuevo/', {
            'titulo': 'Boletin de prueba',
            'contenido': '<p>Contenido de prueba</p>',
            'accion': 'guardar'
        })
        cls.boletin = Boletin.objects.latest('id')
        cls.boletin_id = cls.boletin.id
        print(f"-> Boletín creado con ID: {cls.boletin_id}\n")


    def test_editar_boletin_existente(self):
        print("\n-> Ejecutando test_editar_boletin_existente")
        print(f"-> Accediendo a /editor/boletin/{self.boletin_id}/editar/")
        response = self.client.get(f'/editor/boletin/{self.boletin_id}/editar/')
        print(f"-> Respuesta recibida: {response.status_code}")
        print(f"-> Respuesta esperada: 200")
        self.assertEqual(response.status_code, 200)

    def test_editar_boletin_inexistente(self):
        print("\n\n-> Ejecutando test_editar_boletin_inexistente")
        print("-> Accediendo a /editor/boletin/-1/editar/")
        response = self.client.get('/editor/boletin/-1/editar/')
        print(f"-> Respuesta recibida: {response.status_code}")
        print(f"-> Respuesta esperada: 404")
        self.assertEqual(response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'boletin_id'):
            Boletin.objects.filter(id=cls.boletin_id).delete()
        print("\n=== Finalizando pruebas de edición de boletines existentes e inexistentes ===")



if __name__ == '__main__':
    unittest.main()
    