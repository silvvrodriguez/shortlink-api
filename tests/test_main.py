def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "ShortLink API is running"
    }


def test_create_link(client):
    response = client.post(
        "/links",
        json={
            "url": "https://www.python.org/"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["original_url"] == "https://www.python.org/"
    assert len(data["short_code"]) == 6
    assert data["short_url"].endswith(data["short_code"])


def test_redirect_link(client):
    create_response = client.post(
        "/links",
        json={
            "url": "https://www.python.org/"
        }
    )

    short_code = create_response.json()["short_code"]

    response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "https://www.python.org/"


def test_missing_short_code(client):
    response = client.get(
        "/does-not-exist",
        follow_redirects=False
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Short link not found"
    }