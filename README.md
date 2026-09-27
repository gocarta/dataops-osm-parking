⚠️ WORK IN PROGRESS

# dataops-osm-parking
> Parking Lots and Garages within Hamilton County from [OpenStreetMap](https://www.openstreetmap.org/) via [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)

## license
The data is licensed under ODbL (Open Database License) because it comes from OpenStreetMap.  All code in this repo is released into the public domain as CC0-1.0.

## background
We built this dataset to feed a parking layer in the [Chattanooga Parking Network Map](https://map.chattanoogaparking.net/).

## frequency
This pipeline is run once a day and on-demand.

## query
```
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
```

## columns
| column | example | description |
| :--- | :--- | :--- |
| **@id** | `45509897` | The unique OpenStreetMap identifier. |
| **@type** | `way` | The OpenStreetMap type. |
| **access** | `"yes"` | The access field value in OSM. |
| **amenity** | `"parking"` | This is always parking. |
| **fee** | `"yes"` | Whether there is a fee for parking. |
| **parking** | `"multi-storey"` | The type of parking, which can be "surface" or "multi-storey". |
| **building** | `"parking"` | The type of building (only applicable if it's a building). |
| **name** | `"CARTA South Garage"` | The name of the parking location |
| **building:levels** | `6` | The number of levels/stories in the building |
| **operator** | `"CARTA"` | The name of the company or authority operating the parking the parking |
| **operator:type** | `"public"` | The type of the operator (e.g. public or private) |
| **roof:shape** | `"flat"` | The shape of the roof |
| **wheelchair** | `"yes"` | Whether the location is accessible using a wheelchair |

## download links
- [metadata](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/meta.json)
- [csv](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.csv)
- [geojson (points)](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.points.geojson)
- [geojson (polygons)](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.polygons.geojson) 
- [geoparquet](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.parquet)
- [json](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.json)
- [json lines](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.jsonl)
- [shapefile (points)](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.points.shp.zip)
- [shapefile (polygons)](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.polygons.shp.zip)
- [tsv](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.tsv)

## preview links
- You can view the geojson of points on a map using [geojson.io](https://geojson.io/#data=data:text/x-url,https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.points.geojson).
- You can view the geojson of polygons on a map using [geojson.io](https://geojson.io/#data=data:text/x-url,https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.polygons.geojson).
- You can view the shapefile of points on a map using [shapefile.io](https://shapefile.io?url=https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.points.shp.zip).
- You can view the shapefile of polygons on a map using [shapefile.io](https://shapefile.io?url=https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.polygons.shp.zip).
- You can query the data with SQL using [duckdb](https://shell.duckdb.org/#queries=v0,CREATE-TABLE-dataset-AS-SELECT-*-FROM-'s3://gocarta/public/data/osm_parking/v1/data.parquet'~,Describe-dataset~).

## support
Post an issue [here](https://github.com/gocarta/dataops-osm-parking/issues) or email the package author at DanielDufour@gocarta.org.
