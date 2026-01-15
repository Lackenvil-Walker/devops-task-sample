import os
import tempfile
from fastapi.testclient import TestClient

# Point app at a sqlite DB for tests (no Postgres needed)
db_fd, db_path = tempfile.mkstemp(prefix="test_app_", suffix=".db")
os.close(db_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from app.main import app  # noqa: E402

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.text == "ok"

def test_submit_and_render():
    r = client.post("/submit", data={"text": "hello"})
    assert r.status_code in (200, 303)
    r2 = client.get("/")
    assert r2.status_code == 200
    assert "hello" in r2.text
