from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.test import APITestCase

from users.models import Category, Color, Item, Location

User = get_user_model()


class APITestItemFilters(APITestCase):
    def setUp(self):

        Category.objects.all().delete()
        Color.objects.all().delete()
        Location.objects.all().delete()
        Item.objects.all().delete()

        self.user = User.objects.create_user(username="testuser", password="password")

        self.category1 = Category.objects.create(name="Acessórios", category_id="01")
        self.category2 = Category.objects.create(name="Eletrônicos", category_id="02")

        self.color1 = Color.objects.create(name="Preto", color_id="01")
        self.color2 = Color.objects.create(name="Branco", color_id="02")

        self.location1 = Location.objects.create(name="Biblioteca", location_id="01")
        self.location2 = Location.objects.create(name="Sala de Aula", location_id="02")

        self.item1 = Item.objects.create(
            user=self.user,
            name="Relógio",
            category=self.category1,
            color=self.color1,
            location=self.location1,
            status="found",
        )
        self.item2 = Item.objects.create(
            user=self.user,
            name="Celular",
            category=self.category2,
            color=self.color2,
            location=self.location2,
            status="lost",
        )

    def test_filter_by_category_name(self):
        response = self.client.get("/api/items/?category_name=Acessórios")
        print("Resposta da API (Categoria):", response.data)
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["category_name"] == "Acessórios"

    def test_filter_by_color_name(self):
        response = self.client.get("/api/items/?color_name=Preto")
        print("Resposta da API (Cor):", response.data)
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["color_name"] == "Preto"

    def test_filter_by_status(self):
        response = self.client.get("/api/items/?status=found")
        print("Resposta da API (Status 'found'):", response.data)
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "found"

        response = self.client.get("/api/items/?status=lost")
        print("Resposta da API (Status 'lost'):", response.data)
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "lost"

    def test_filter_by_multiple_parameters(self):
        response = self.client.get("/api/items/?category_name=Acessórios&color_name=Preto")
        print("Resposta da API (Filtros múltiplos):", response.data)
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["category_name"] == "Acessórios"
        assert response.data["results"][0]["color_name"] == "Preto"

        response = self.client.get("/api/items/?category_name=Acessórios&color_name=Branco")
        print("Resposta da API (Filtros múltiplos sem resultados):", response.data)
        assert len(response.data["results"]) == 0

    def test_no_filters(self):
        response = self.client.get("/api/items/")
        print("Resposta da API (Sem filtros):", response.data)
        assert len(response.data["results"]) == 2

    def test_no_results(self):
        response = self.client.get("/api/items/?category_name=NãoExiste")
        print("Resposta da API (Sem resultados):", response.data)
        assert len(response.data["results"]) == 0

    def test_update_item(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Relógio Atualizado"}
        response = self.client.patch(f"/api/items/{self.item1.id}/", data)
        assert response.status_code == 200
        self.item1.refresh_from_db()
        assert self.item1.name == "Relógio Atualizado"

    def test_pagination(self):
        response = self.client.get("/api/items/?page=1")
        assert response.status_code == 200
        assert "results" in response.data
        assert "count" in response.data
        assert "next" in response.data or "previous" in response.data
        assert len(response.data["results"]) <= 10

    def test_search_by_name(self):
        response = self.client.get("/api/items/?search=Relógio")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Relógio"

    def test_search_by_description(self):
        self.item2.description = "Celular encontrado"
        self.item2.save()

        response = self.client.get("/api/items/?search=Celular")
        assert response.status_code == 200
        assert len(response.data["results"]) >= 1
        assert response.data["results"][0]["description"] == "Celular encontrado"

    def test_search_by_category_name(self):
        response = self.client.get("/api/items/?search=Acessórios")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["category_name"] == "Acessórios"

    def test_search_by_location_name(self):
        response = self.client.get("/api/items/?search=Biblioteca")
        assert response.status_code == 200
        assert len(response.data["results"]) >= 1
        assert response.data["results"][0]["location_name"] == "Biblioteca"

    def test_ordering_by_created_at(self):
        response = self.client.get("/api/items/?ordering=created_at")
        assert response.status_code == 200
        results = response.data["results"]
        assert len(results) == 2
        assert results[0]["created_at"] <= results[1]["created_at"]

    def test_ordering_by_found_lost_date(self):
        self.item1.found_lost_date = now() - timedelta(days=1)
        self.item2.found_lost_date = now()
        self.item1.save()
        self.item2.save()

        response = self.client.get("/api/items/?ordering=found_lost_date")
        assert response.status_code == 200
        results = response.data["results"]
        results = [r for r in results if r["found_lost_date"] is not None]
        assert len(results) >= 2
        assert results[0]["found_lost_date"] <= results[1]["found_lost_date"]

    def test_reverse_ordering(self):
        response = self.client.get("/api/items/?ordering=-created_at")
        assert response.status_code == 200
        results = response.data["results"]
        assert len(results) == 2
        assert results[0]["created_at"] >= results[1]["created_at"]
