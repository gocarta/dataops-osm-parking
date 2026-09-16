⚠️ WORK IN PROGRESS

# dataops-osm-parking
> Parking Lots and Garages within Hamilton County from [OpenStreetMap](https://www.openstreetmap.org/) 

## background
We built this dataset to feed a parking layer in the [Chattanooga Parking Network Map](https://map.chattanoogaparking.net/).

## frequency
Unfortunately, this dataset is manually updated at the moment by going to [Overpass Ultra](https://overpass-ultra.us/), running the following query, and then downloading as GeoJSON.

## query
```
area
  [place=county]
  ["wikidata"="Q188376"]
  ["name"="Hamilton County"]->.a;

(
  wr["amenity"="parking"](area.a);
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
- [geojson](https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.polygons.geojson)

## preview links
- You can view the geojson on a map using [geojson.io](https://geojson.io/#data=data:text/x-url,https://gocarta.s3.us-east-2.amazonaws.com/public/data/osm_parking/v1/data.polygons.geojson).

## support
Post an issue [here](https://github.com/gocarta/dataops-cloud-vehicle-locations/issues) or email the package author at DanielDufour@gocarta.org.
