def test_get_all_crops(client):
    res = client.get("/api/crops/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_crop_not_found(client):
    res = client.get("/api/crops/99999")
    assert res.status_code == 404


def test_get_all_seeds(client):
    res = client.get("/api/seeds/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_seed_not_found(client):
    res = client.get("/api/seeds/99999")
    assert res.status_code == 404


def test_get_all_fertilizers(client):
    res = client.get("/api/fertilizers/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_fertilizer_not_found(client):
    res = client.get("/api/fertilizers/99999")
    assert res.status_code == 404
