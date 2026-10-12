import pytest
from app import app, members


@pytest.fixture()
def client():
    original = list(members)
    members.clear()
    members.append({"id": 1, "name": "Arun", "plan": "Monthly"})
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client
    members.clear()
    members.extend(original)


def test_home_returns_application_name(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["application"] == "ACEest Fitness & Gym"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_list_members(client):
    response = client.get("/members")
    assert response.status_code == 200
    assert response.get_json() == [{"id": 1, "name": "Arun", "plan": "Monthly"}]


def test_add_member(client):
    response = client.post("/members", json={"name": " Priya ", "plan": "Quarterly"})
    assert response.status_code == 201
    assert response.get_json() == {"id": 2, "name": "Priya", "plan": "Quarterly"}


@pytest.mark.parametrize("payload", [
    {}, {"name": "", "plan": "Monthly"}, {"name": "Priya", "plan": ""},
    {"name": 12, "plan": "Monthly"},
])
def test_add_member_rejects_invalid_payload(client, payload):
    assert client.post("/members", json=payload).status_code == 400


def test_add_member_rejects_non_json(client):
    response = client.post("/members", data="not-json", content_type="text/plain")
    assert response.status_code == 400
