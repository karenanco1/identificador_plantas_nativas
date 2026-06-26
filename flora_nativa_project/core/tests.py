from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Region, Planta


class RegionModelTest(TestCase):
    def test_crear_region(self):
        region = Region.objects.create(nombre="Metropolitana", numero=13)
        self.assertEqual(str(region), "Metropolitana")
        self.assertEqual(region.numero, 13)


class PlantaModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(nombre="Valparaíso", numero=5)
        self.planta = Planta.objects.create(
            nombre_comun="Boldo",
            nombre_cientifico="Peumus boldus",
            uso_principal="MED",
            ubicacion_especifica="Laderas soleadas de la cordillera",
        )
        self.planta.regiones.add(self.region)

    def test_crear_planta(self):
        self.assertEqual(str(self.planta), "Boldo (Peumus boldus)")

    def test_relacion_region(self):
        self.assertIn(self.region, self.planta.regiones.all())

    def test_planta_sin_perenual_id(self):
        self.assertIsNone(self.planta.perenual_id)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registro_get(self):
        response = self.client.get(reverse("registro"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registro.html")

    def test_registro_post(self):
        response = self.client.post(reverse("registro"), {
            "username": "testuser",
            "password1": "testpass123!",
            "password2": "testpass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_post(self):
        User.objects.create_user(username="testuser", password="testpass123!")
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass123!",
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        User.objects.create_user(username="testuser", password="testpass123!")
        self.client.login(username="testuser", password="testpass123!")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.region = Region.objects.create(nombre="Maule", numero=7)
        self.planta = Planta.objects.create(
            nombre_comun="Quillay",
            nombre_cientifico="Quillaja saponaria",
            uso_principal="MED",
        )
        self.planta.regiones.add(self.region)

    def test_home_status(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_home_filtro_region(self):
        response = self.client.get(reverse("home"), {"region": self.region.id})
        self.assertContains(response, "Quillay")

    def test_home_busqueda(self):
        response = self.client.get(reverse("home"), {"q": "Quillay"})
        self.assertContains(response, "Quillay")

    def test_home_busqueda_sin_resultados(self):
        response = self.client.get(reverse("home"), {"q": "Noexiste"})
        self.assertNotContains(response, "Quillay")


class DetalleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.planta = Planta.objects.create(
            nombre_comun="Araucaria",
            nombre_cientifico="Araucaria araucana",
            uso_principal="ORN",
        )

    def test_detalle_existente(self):
        response = self.client.get(reverse("detalle_planta", args=[self.planta.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "detalle.html")

    def test_detalle_no_existente(self):
        response = self.client.get(reverse("detalle_planta", args=[999]))
        self.assertEqual(response.status_code, 404)
