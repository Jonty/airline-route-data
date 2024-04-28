#!/usr/bin/python
import sys
import json
from collections import defaultdict
import time

from curl_cffi import requests
import lxml.html
from geopy.distance import geodesic

if __name__ == "__main__":

    print("Fetching airports list...")
    response = requests.get(
        "https://www.flightsfrom.com/airports", impersonate="chrome"
    )
    try:
        airports_json = json.loads(response.content)
    except json.decoder.JSONDecodeError as e:
        print("Failed to load airport JSON, page body was: '%s'" % response.content)
        sys.exit(1)

    iatas = [airport["IATA"] for airport in airports_json["response"]["airports"]]

    airports = defaultdict(dict)

    while iatas:
        iata = iatas.pop()
        if iata in airports:
            continue

        print("Fetching #%s: %s" % (len(airports), iata))

        response = requests.get(
            "https://www.flightsfrom.com/%s/destinations" % iata, impersonate="chrome"
        )
        root = lxml.html.document_fromstring(response.content)
        metadata_nodes = root.xpath('//script[contains(., "window.airport")]')
        metadata_tag = metadata_nodes[0].text_content()
        metadata_bits = metadata_tag.split("window.")

        metadata = {}
        for bit in metadata_bits:
            split = bit.find("=")
            if split != -1:
                metadata[bit[:split].strip()] = json.loads(bit.strip()[split + 2 : -1])

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
        airport = {
            field.lower(): metadata["airport"][field] for field in airport_fields
        }
        if airport["elevation"]:
            airport["elevation"] = int(airport["elevation"])

        routes = []
        for route in metadata["routes"]:
            carrier_fields = [
                "name",
                "IATA",
            ]

            carriers = []
            for aroute in route["airlineroutes"]:
                is_passenger = (
                    aroute["airline"]["is_scheduled_passenger"] == "1"
                    or aroute["airline"]["is_nonscheduled_passenger"] == "1"
                )
                is_active = aroute["airline"]["active"]
                if is_active and is_passenger:
                    carriers.append(
                        {
                            field.lower(): aroute["airline"][field]
                            for field in carrier_fields
                        }
                    )

            orig_ll = (airport["latitude"], airport["longitude"])
            dest_ll = (route["airport"]["latitude"], route["airport"]["longitude"])
            distance = int(geodesic(orig_ll, dest_ll).km)

            routes.append(
                {
                    "carriers": carriers,
                    "km": distance,
                    "min": int(route["common_duration"]),
                    "iata": route["iata_to"],
                }
            )

            iatas.append(route["iata_to"])

        airport["routes"] = routes
        airports[iata] = airport

        time.sleep(1)

    with open("airline_routes.json", "w") as f:
        f.write(json.dumps(airports, indent=4, sort_keys=True, separators=(",", ": ")))
