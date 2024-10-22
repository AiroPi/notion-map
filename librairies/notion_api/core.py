from __future__ import annotations

from typing import Any, Literal, TypedDict, Union

import httpx

MISSING: Any = object()


class SearchSort(TypedDict):
    direction: Literal["ascending", "descending"]
    timestamp: Literal["last_edited_time"]


class SearchFilter(TypedDict):
    value: Literal["page", "database"]
    property: Any


class DatabaseQuerySortProperty(TypedDict):
    property: str
    direction: Literal["ascending", "descending"]


class DatabaseQuerySortTimestamp(TypedDict):
    timestamp: Literal["last_edited_time", "created_time"]
    direction: Literal["ascending", "descending"]


DatabaseQuerySort = Union[DatabaseQuerySortProperty, DatabaseQuerySortTimestamp]


class NotionClient:
    BASE = "https://api.notion.com/v1"

    def __init__(self, token: str):
        self.token = token
        self.client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
        }
        self.client = await httpx.AsyncClient(
            headers=headers, default_encoding="utf-8"
        ).__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any):
        if self.client is not None:
            await self.client.aclose()
        self.client = None

    async def _request(self, method: str, uri: str, **kwargs: Any):
        if self.client is None:
            raise RuntimeError("Please use this class as a context manager.")
        return await self.client.request(method, uri, **kwargs)

    async def _get(self, uri: str, params: dict[str, Any] = MISSING):
        kwargs: dict[str, Any] = {}
        if params is not MISSING:
            kwargs["params"] = params
        return await self._request("GET", uri, **kwargs)

    async def _post(
        self, uri: str, json: dict[str, Any] = MISSING, params: dict[str, Any] = MISSING
    ):
        kwargs: dict[str, Any] = {}
        if json is not MISSING:
            kwargs["json"] = json
        if params is not MISSING:
            kwargs["params"] = params
        return await self._request("POST", uri, **kwargs)

    async def search(
        self,
        query: str,
        sort: SearchSort = MISSING,
        filter: SearchFilter = MISSING,
        start_cursor: str = MISSING,
        page_size: int = MISSING,
    ):
        json: dict[str, Any] = dict(query=query)
        if sort is not MISSING:
            json["sort"] = sort
        if filter is not MISSING:
            json["filter"] = filter
        if start_cursor is not MISSING:
            json["start_cursor"] = start_cursor
        if page_size is not MISSING:
            json["page_size"] = page_size

        return await self._post(
            self.BASE + "/search",
            json=json,
        )

    async def query_database(
        self,
        database_id: str,
        filter_properties: list[str] = MISSING,
        sorts: list[DatabaseQuerySort] = MISSING,
    ):
        json: dict[str, Any] = {}
        if sorts is not MISSING:
            json["sorts"] = sorts

        params = MISSING
        if filter_properties is not MISSING:
            params = {"filter_properties": filter_properties}

        response = await self._post(
            self.BASE + f"/databases/{database_id}/query", json=json, params=params
        )
        return response.json()

    async def retrieve_database(
        self,
        database_id: str,
    ) -> dict[str, Any]:
        response = await self._get(self.BASE + f"/databases/{database_id}")
        return response.json()
