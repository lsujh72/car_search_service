from fastapi.testclient import TestClient

from src.location.models import Location
from src.cargo.models import Cargo


def test_create(
    app_client: TestClient,
    create_cargo: Cargo,
    create_location_1: Location,
    create_location_2: Location,
) -> None:
    payload = {
        "id": create_cargo.id,
        "location_pick_up_zip": create_location_1.zip,
        "location_delivery_zip": create_location_2.zip,
        "weight": create_cargo.weight,
        "description": create_cargo.description,
    }
    resp = app_client.post("/cargo/", json=payload)
    assert resp.status_code == 201, resp.text


def test_list(app_client: TestClient, create_cargo: Cargo) -> None:
    resp = app_client.get("/cargo/")
    cargo = resp.json()
    assert resp.status_code == 200
    assert len(cargo) == 1
    assert cargo[0]["weight"] == 666


def test_get(app_client: TestClient, create_cargo: Cargo) -> None:
    resp = app_client.get(f"/cargo/{create_cargo.id}")
    assert resp.status_code == 200
    assert "cars" in resp.json()


def test_update(
    app_client: TestClient,
    create_cargo: Cargo,
) -> None:
    payload = {"weight": 500, "description": create_cargo.description}
    resp = app_client.patch(f"/cargo/{create_cargo.id}", json=payload)
    cargo = resp.json()
    assert resp.status_code == 201, resp.text
    assert cargo["weight"] == 500


def test_delete(app_client: TestClient, create_cargo: Cargo) -> None:
    resp = app_client.delete(f"/cargo/{create_cargo.id}")
    assert resp.status_code == 204
