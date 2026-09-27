# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datablob",
#     "requests",
#     "simple-env",
# ]
# ///
import datablob
import requests
from shapely.geometry import (
    Polygon,
    MultiPolygon,
    mapping,
)
import simple_env as se

AWS_BUCKET_NAME = se.get("AWS_BUCKET_NAME")
if not AWS_BUCKET_NAME:
    raise Exception("[dataops-osm-parking] missing AWS_BUCKET_NAME")

AWS_BUCKET_PATH = se.get("AWS_BUCKET_PATH")
if not AWS_BUCKET_PATH:
    raise Exception("[dataops-osm-parking] missing AWS_BUCKET_PATH")

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# query grabs building and lots whose primary use is parking
# AND buildings with multi-storey parking garages even if primary use isn't clearly parking

OVERPASS_QUERY = """
[out:json][timeout:90];

area
  [place=county]
  ["wikidata"="Q188376"]
  ["name"="Hamilton County"]->.a;

(
  wr["amenity"="parking"](area.a);
  wr["parking"="multi-storey"](area.a);
);

out geom;
""".strip()

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "gocarta/dataops-osm-parking (danieldufour@gocarta.org)",
}
payload = {"data": OVERPASS_QUERY}
response = requests.post(OVERPASS_URL, data=payload, headers=headers)
response.raise_for_status()
data = response.json()


def osm_element_to_row(element):
    tags = element.get("tags", {})

    if element["type"] == "way":
        coords = [(p["lon"], p["lat"]) for p in element["geometry"]]

        if len(coords) < 4:
            return None

        if coords[0] != coords[-1]:
            coords.append(coords[0])

        geom = Polygon(coords)

    elif element["type"] == "relation":
        outers = []

        for member in element.get("members", []):
            if member.get("role") == "outer" and "geometry" in member:
                coords = [(p["lon"], p["lat"]) for p in member["geometry"]]

                if len(coords) < 4:
                    continue

                if coords[0] != coords[-1]:
                    coords.append(coords[0])

                outers.append(Polygon(coords))

        if not outers:
            return None

        geom = outers[0] if len(outers) == 1 else MultiPolygon(outers)

    else:
        return None

    return {
        **tags,
        "@id": element["id"],
        "@type": element["type"],
        "@lat": geom.centroid.y,
        "@lon": geom.centroid.x,
        "@geometry": mapping(geom),
    }


rows = []
for el in data["elements"]:
    row = osm_element_to_row(el)
    if row:
        rows.append(row)

client = datablob.DataBlobClient(
    bucket_name=AWS_BUCKET_NAME, bucket_path=AWS_BUCKET_PATH
)

COLUMN_NAMES = [
    "@id",
    "@type",
    "name",
    "@lat",
    "@lon",
    "access",
    "access:conditional",
    "addr:city",
    "addr:housenumber",
    "addr:postcode",
    "addr:state",
    "addr:street",
    "amenity",
    "check_date",
    "check_date:opening_hours",
    "fee",
    "landuse",
    "parking",
    "building",
    "building:levels",
    "opening_hours",
    "operator",
    "operator:short",
    "operator:type",
    "operator:wikidata",
    "operator:wikipedia",
    "park_ride",
    "parking",
    "parking_space",
    "payment:app",
    "payment:cards",
    "payment:credit_cards",
    "payment:debit_cards",
    "payment:parkmobile",
    "roof:levels",
    "roof:shape",
    "smoothness",
    "supervised",
    "surface",
    "toilets",
    "type",
    "vending",
    "wheelchair",
    "@geometry",
]

# delete columns not in COLUMN_NAMES
for row in rows:
    for key in list(row.keys()):
        if key not in COLUMN_NAMES:
            del row[key]

client.update_dataset(
    name="osm_parking",
    description="Parking Lots and Garages within Hamilton County from OpenStreetMap via Overpass API",
    version="1",
    data=rows,
    column_names=COLUMN_NAMES,
    json=True,
    jsonl=True,
    latitude_key="@lat",
    longitude_key="@lon",
    polygon_key="@geometry",
    parquet=True,
    xlsx=False,
)

print(f"[dataops-osm-parking] updated {len(rows)} rows")
