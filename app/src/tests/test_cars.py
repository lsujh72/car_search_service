from fastapi.testclient import TestClient

from src.location.models import Location
from src.car.models import Car


def test_create(
    app_client: TestClient, create_car: Car, create_location: Location
) -> None:
    payload = {
        "id": create_car.id,
        "unique_number": "9752Q",
        "carrying": create_car.carrying,
        "location_current_id": create_location.id,
    }
    resp = app_client.post("/cars", json=payload)
    assert resp.status_code == 201, resp.text


def test_update(
    app_client: TestClient, create_car: Car, create_location_1: Location
) -> None:
    payload = {"carrying": 800, "zip": create_location_1.zip}
    resp = app_client.patch(f"/cars/{create_car.id}", json=payload)
    cargo = resp.json()
    assert resp.status_code == 201, resp.text
    assert cargo["carrying"] == 800
