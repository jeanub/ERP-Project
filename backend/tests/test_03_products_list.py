import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from model_bakery import baker

def auth_headers(client):
    U = get_user_model()
    u, _ = U.objects.update_or_create(username="jean", defaults={"is_active": True})
    u.set_password("x"); u.save()
    r = client.post("/api/auth/token/", {"username":"jean","password":"x"},
                    content_type="application/json")
    assert r.status_code == 200, r.content
    return {"HTTP_AUTHORIZATION": f"Bearer {r.json()['access']}"}

@pytest.mark.django_db
def test_products_lista_con_auth(client):
    h = auth_headers(client)
    baker.make("products.Product", sku="SKU-001", name="Teclado",
               price=Decimal("15000"), stock=5)
    r = client.get("/api/products/", **h)
    assert r.status_code == 200, r.content
