import pytest

from helpers import fake_room


@pytest.fixture()
def delete_room_after(auth_client):
    room_name = None

    def _set_room(name):
        nonlocal room_name
        room_name = name

    yield _set_room

    rooms = auth_client.get("/api/room").json()["rooms"]
    room_id = next((r["roomid"] for r in rooms if str(r["roomName"]) == str(room_name)), None)
    if room_id:
        auth_client.delete(f"/api/room/{room_id}")


@pytest.fixture()
def create_room(auth_client):
    data = fake_room()
    auth_client.post("/api/room", json=data)

    rooms = auth_client.get("/api/room").json()["rooms"]
    room_id = next(
        (r["roomid"] for r in rooms if str(r["roomName"]) == str(data["roomName"])),
        None,
    )

    yield {"id": room_id, "name": data["roomName"]}

    if room_id:
        auth_client.delete(f"/api/room/{room_id}")
