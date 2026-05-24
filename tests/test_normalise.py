import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    yield app.test_client()

def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200

def test_string_input(client):
    r = client.post('/normalise',
        json={"data": '{"name": "Mayur"}'},
        content_type='application/json')
    assert r.status_code == 200
    assert r.json['input_type'] == 'str'
    assert r.json['normalised'] == {"name": "Mayur"}

def test_array_input(client):
    r = client.post('/normalise',
        json={"data": [{"name": "Mayur"}, {"name": "Other"}]},
        content_type='application/json')
    assert r.status_code == 200
    assert r.json['normalised'] == {"name": "Mayur"}

def test_null_input(client):
    r = client.post('/normalise',
        json={"data": None},
        content_type='application/json')
    assert r.status_code == 200
    assert r.json['normalised'] == {}

def test_dict_input(client):
    r = client.post('/normalise',
        json={"data": {"name": "Mayur", "score": 99}},
        content_type='application/json')
    assert r.status_code == 200
    assert r.json['normalised']['name'] == "Mayur"

def test_missing_field(client):
    r = client.post('/normalise',
        json={"wrong": "value"},
        content_type='application/json')
    assert r.status_code == 422