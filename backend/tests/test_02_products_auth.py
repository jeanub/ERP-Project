import pytest

@pytest.mark.django_db
def test_products_requiere_auth(client):
    r = client.get("/api/products/")
    assert r.status_code in (401, 403)
