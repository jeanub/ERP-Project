import pytest

@pytest.mark.django_db
def test_ping_abierto(client):
    r = client.get("/api/ping/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
