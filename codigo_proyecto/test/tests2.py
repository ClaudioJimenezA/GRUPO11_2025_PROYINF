import unittest
import requests

# === CONFIGURACIÓN GENERAL ===
PORT = 8000
base_url = f"http://127.0.0.1:{PORT}"

# Usuarios por rol
EDITOR_USER = "wario"
EDITOR_PASS = "editor"

LECTOR_USER = "waluigi"
LECTOR_PASS = "lector"


class TestEditorEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url_login = f"{base_url}/login/"
        cls.url_edicion = f"{base_url}/editor/boletin/1/editar/"
        cls.url_editor_view = f"{base_url}/editor/"

    def test_editor_puede_editar(self):
        session = requests.Session()
        session.post(self.url_login, data={"username": EDITOR_USER, "password": EDITOR_PASS})
        response = session.get(self.url_editor_view)
        print("Editor accede a vista del editor:", response.status_code)
        self.assertIn(response.status_code, [200, 302])

    def test_lector_no_puede_editar(self):
        session = requests.Session()
        session.post(self.url_login, data={"username": LECTOR_USER, "password": LECTOR_PASS})
        response = session.get(self.url_editor_view)
        print("Lector intenta acceder al editor(esperado 403):", response.status_code)
        self.assertEqual(response.status_code, 403)

    @classmethod
    def tearDownClass(cls):
        print("Finalizado: Pruebas de acceso a edición\n")



class TestGestionPDFsEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url_login = f"{base_url}/login/"
        cls.url_pdfs = f"{base_url}/pdfs/"

    def test_editor_puede_ver_pdfs(self):
        session = requests.Session()
        session.post(self.url_login, data={"username": EDITOR_USER, "password": EDITOR_PASS})
        acceso = session.get(self.url_pdfs)
        print("Editor accede a PDFs:", acceso.status_code)
        self.assertIn(acceso.status_code, [200, 302])

    def test_lector_puede_ver_pdfs(self):
        session = requests.Session()
        session.post(self.url_login, data={"username": LECTOR_USER, "password": LECTOR_PASS})
        acceso = session.get(self.url_pdfs)
        print("Lector accede a PDFs:", acceso.status_code)
        self.assertIn(acceso.status_code, [200, 302])

    @classmethod
    def tearDownClass(cls):
        print("Finalizado: Pruebas de acceso a PDFs\n")



class TestPruebasInversas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url_login = f"{base_url}/login/"
        cls.url_edicion = f"{base_url}/editor/boletin/1/editar/"
        cls.url_pdfs = f"{base_url}/pdfs/"

    def test_editor_no_deberia_fallar_en_pdf(self):
        session = requests.Session()
        session.post(self.url_login, data={"username": EDITOR_USER, "password": EDITOR_PASS})
        acceso = session.get(self.url_pdfs)
        print("Editor accede a PDFs (esperado 200/302):", acceso.status_code)
        self.assertIn(acceso.status_code, [200, 302])

    def test_lector_no_deberia_editar(self):
        session = requests.Session()
        session.post(self.url_login, data={"username": LECTOR_USER, "password": LECTOR_PASS})
        edit = session.post(self.url_edicion, data={
            "titulo": "Edición no permitida",
            "contenido": "No debería poder editar",
            "accion": "guardar"
        })
        print("Lector intenta editar (esperado 403):", edit.status_code)
        self.assertEqual(edit.status_code, 403)

    @classmethod
    def tearDownClass(cls):
        print("Finalizando pruebas inversas de validación de roles\n")



if __name__ == '__main__':
    unittest.main()

