#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
