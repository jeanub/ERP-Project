import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from model_bakery import baker

def auth_headers(client, username="jean", password="x"):
    User = get_user_model()
    u = User.objects.create_user(username=username, password=password)
    r = client.post("/api/auth/token/", {"username": username, "password": password},
                    content_type="application/json")
    assert r.status_code == 200, r.content
    access = r.json()["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {access}"}

@pytest.mark.django_db
def test_ping_abierto(client):
    r = client.get("/api/ping/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

@pytest.mark.django_db
def test_products_requiere_auth(client):
    r = client.get("/api/products/")
    assert r.status_code in (401, 403), f"Debería requerir auth, devolvió {r.status_code}"

@pytest.mark.django_db
def test_products_lista_con_auth(client):
    h = auth_headers(client)
    # seed mínimo
    baker.make("products.Product", sku="SKU-001", name="Teclado", price=Decimal("15000"), stock=5)
    r = client.get("/api/products/", **h)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, (list, dict))

@pytest.mark.django_db
def test_orden_confirm_descuenta_stock(client):
    h = auth_headers(client)
    cust = baker.make("customers.Customer")
    prod = baker.make("products.Product", stock=5, price=Decimal("10"))
    # crea orden
    o = client.post("/api/orders/", {"customer": cust.id, "status": "draft", "total": "0"},
                    content_type="application/json", **h)
    assert o.status_code == 201, o.content
    oid = o.json()["id"]
    # item
    it = client.post("/api/order-items/", {"order": oid, "product": prod.id, "quantity": 2,
                    "unit_price": "10", "line_total": "20"},
                    content_type="application/json", **h)
    assert it.status_code == 201, it.content
    # confirmar
    c = client.post(f"/api/orders/{oid}/confirm/", **h)
    assert c.status_code == 200, c.content
    prod.refresh_from_db()
    assert prod.stock == 3
