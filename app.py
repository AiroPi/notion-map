import os
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

from librairies.notion_api import NotionClient

try:
    import dotenv
except ImportError:
    pass
else:
    dotenv.load_dotenv()

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
DATABASE_SOURCE_ID = os.environ["DATABASE_SOURCE_ID"]

# LATITUDE_COLUMN_NAME = "Latitude"
# LONGITUDE_COLUMN_NAME = "Longitude2"

with open("./pages/index.html", "r") as f:
    PAGE = f.read()

app = FastAPI()
notion_client = NotionClient(NOTION_API_KEY)


class DatabaseGetter:
    def __init__(self, database_id: str):
        self.database_id = database_id
        self._database_data: Optional[dict[str, Any]] = None

    async def get(self) -> dict[str, Any]:
        if self._database_data is None:
            async with NotionClient(NOTION_API_KEY) as nc:
                self._database_data = await nc.retrieve_database(self.database_id)
        return self._database_data


database = DatabaseGetter(DATABASE_SOURCE_ID)


@app.get("/locations")
async def locations():
    # db = await database.get()
    # latitude_column_id = next(
    #     p["id"] for p in db["properties"].values() if p["name"] == LATITUDE_COLUMN_NAME
    # )
    # longitude_column_id = next(
    #     p["id"] for p in db["properties"].values() if p["name"] == LONGITUDE_COLUMN_NAME
    # )

    async with NotionClient(NOTION_API_KEY) as c:
        raw_locations = await c.query_database(
            DATABASE_SOURCE_ID,
            # filter_properties=["title"],
        )

    def get_property_by_id(
        properties: dict[str, dict[str, Any]], id: str
    ) -> dict[str, Any]:
        return next(p for p in properties.values() if p["id"] == id)

    def extract(l: dict[str, Any]) -> Optional[tuple[str, float, float, str]]:
        longitude = l["properties"]["Longitude"]["number"]
        latitude = l["properties"]["Latitude"]["number"]
        title = get_property_by_id(l["properties"], "title")

        if longitude and latitude and title["title"]:
            return (
                title["title"][0]["plain_text"],
                latitude,
                longitude,
                l["public_url"],
            )

    locations = [
        extracted for l in raw_locations["results"] if (extracted := extract(l))
    ]

    return locations


@app.get("/map")
async def map():
    return HTMLResponse(PAGE)


@app.get("/")
def read_root():
    return RedirectResponse("/map")
