"""Tests module."""
import json
from unittest import mock

import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from pytest_httpx import HTTPXMock

from getwall.application import (
    POSTS_API_URL,
    PostAndComments,
    app,
    container,
    fetch_post_with_comments,
)
from getwall.services import Service


@pytest.fixture
def client(event_loop):
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    event_loop.run_until_complete(client.aclose())


@pytest.mark.asyncio
async def test_get_entities_with_values_in_cache(client):
    service_mock = mock.AsyncMock(spec=Service)
    service_mock.get.return_value = json.dumps(
        {
            "post": {"userId": 1, "id": 1, "title": "title", "body": "text"},
            "comments": [
                {"postId": 1, "id": 1, "name": "name", "email": "email", "body": "text"}
            ],
        }
    )

    with container.service.override(service_mock):
        response = await client.get("/post_with_comments/1")

    assert response.status_code == 200
    assert response.json()["post"]["title"] == "title"


@pytest.mark.asyncio
async def test_get_entities_without_values_cache(client, monkeypatch):
    service_mock = mock.AsyncMock(spec=Service)
    service_mock.get.return_value = None

    fetch_mock = mock.AsyncMock()
    fetch_mock.return_value = PostAndComments.parse_obj(
        {
            "post": {"userId": 1, "id": 1, "title": "new title", "body": "new text"},
            "comments": [
                {
                    "postId": 1,
                    "id": 1,
                    "name": "new name",
                    "email": "new email",
                    "body": "new text",
                }
            ],
        }
    )

    monkeypatch.setattr("getwall.application.fetch_post_with_comments", fetch_mock)
    with container.service.override(service_mock):
        response = await client.get("/post_with_comments/1")

    assert response.status_code == 200
    assert response.json()["post"]["title"] == "new title"


@pytest.mark.asyncio
async def test_get_post_with_comments_without_cache_without_comments(
    client, monkeypatch
):
    service_mock = mock.AsyncMock(spec=Service)
    service_mock.get.return_value = None

    fetch_mock = mock.AsyncMock()
    fetch_mock.return_value = PostAndComments.parse_obj(
        {
            "post": {"userId": 1, "id": 1, "title": "new title", "body": "new text"},
            "comments": [],
        }
    )

    monkeypatch.setattr("getwall.application.fetch_post_with_comments", fetch_mock)
    with container.service.override(service_mock):
        response = await client.get("/post_with_comments/1")

    assert response.status_code == 200
    post = response.json()
    assert post["comments"] == []


@pytest.mark.asyncio
async def test_get_entities_without_post(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=f"{POSTS_API_URL}/1", status_code=200, json={})
    with pytest.raises(Exception) as e:
        await fetch_post_with_comments(1)
    assert e.type == HTTPException
