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
def test_orden_confirm_descuenta_stock(client):
    h = auth_headers(client)
    cust = baker.make("customers.Customer")
    prod = baker.make("products.Product", stock=5, price=Decimal("10"))
    o = client.post("/api/orders/", {"customer": cust.id, "status":"draft", "total":"0"},
                    content_type="application/json", **h)
    assert o.status_code == 201, o.content
    oid = o.json()["id"]

    it = client.post("/api/order-items/", {"order": oid, "product": prod.id,
                    "quantity": 2, "unit_price":"10"},
                    content_type="application/json", **h)
    assert it.status_code == 201, it.content

    c = client.post(f"/api/orders/{oid}/confirm/", **h)
    assert c.status_code == 200, c.content
    prod.refresh_from_db()
    assert prod.stock == 3
