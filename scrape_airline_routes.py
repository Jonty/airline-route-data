#!/usr/bin/python
import sys
import json
from collections import defaultdict

import requests
import lxml.html
from geopy.distance import geodesic

response = requests.get("https://www.flightsfrom.com/airports")
airports_json = response.json()
iatas = [airport["IATA"] for airport in airports_json["response"]["airports"]]

airports = defaultdict(dict)

while iatas:
    iata = iatas.pop()
    if iata in airports:
        continue

    print("Fetching #%s: %s" % (len(airports), iata))

    response = requests.get("https://www.flightsfrom.com/%s/destinations" % iata)
    
    root = lxml.html.document_fromstring(response.content)
    metadata_nodes = root.xpath(
        '//script[starts-with(., "window.airport=")]'
    )
    metadata_tag = metadata_nodes[0].text_content()
    metadata_bits = metadata_tag.split("window.")
    
    metadata = {}
    for bit in metadata_bits:
        split = bit.find("=")
        if split != -1:
            metadata[bit[:split]] = json.loads(bit[split+1:-1])

    airport_fields = [
            "city_name",
            "continent",
            "country",
            "country_code",
            "display_name",
            "elevation",
            "IATA",
            "ICAO",
            "latitude",
            "longitude",
            "name",
            "timezone",
    ]
    airport = {field.lower(): metadata["airport"][field] for field in airport_fields}
    if airport["elevation"]:
        airport["elevation"] = int(airport["elevation"])

    routes = []
    for route in metadata["routes"]:
        orig_ll = (airport["latitude"], airport["longitude"])
        dest_ll = (route["airport"]["latitude"], route["airport"]["longitude"])
        distance = int(geodesic(orig_ll, dest_ll).km)

        routes.append({
            "carriers": list(set(a["carrier_name"] for a in route["airlineroutes"])),
            "km": distance,
            "min": int(route["common_duration"]),
            "iata": route["iata_to"],
        })

        iatas.append(route["iata_to"])

    airport["routes"] = routes
    airports[iata] = airport

with open("airline_routes.json", "w") as f:
    f.write(json.dumps(airports, indent=4, sort_keys=True, separators=(",", ": ")))
