#!/usr/bin/python
import sys
import json
from collections import defaultdict
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import lxml.html
from geopy.distance import geodesic
from fp.fp import FreeProxy

if __name__ == '__main__':
    print("Getting a proxy...")
    proxy = FreeProxy().get(rand=True)
    print("Using %s as a proxy" % proxy)

    options = uc.ChromeOptions()
    options.headless=True
    options.add_argument('--headless')
    options.add_argument('--proxy-server=%s' % proxy)
    driver = uc.Chrome(options=options)

    print("Fetching airports list...")
    driver.get('https://www.flightsfrom.com/airports')
    response = driver.find_elements(By.TAG_NAME, 'body')[0].text
    try:
        airports_json = json.loads(response)
    except json.decoder.JSONDecodeError as e:
        print("Failed to load airport JSON, page body was: '%s'" % response)
        sys.exit(1)

    iatas = [airport["IATA"] for airport in airports_json["response"]["airports"]]

    airports = defaultdict(dict)

    while iatas:
        iata = iatas.pop()
        if iata in airports:
            continue

        print("Fetching #%s: %s" % (len(airports), iata))

        driver.get("https://www.flightsfrom.com/%s/destinations" % iata)
        root = lxml.html.document_fromstring(driver.page_source)
        metadata_nodes = root.xpath(
            '//script[contains(., "window.airport")]'
        )
        metadata_tag = metadata_nodes[0].text_content()
        metadata_bits = metadata_tag.split("window.")
        
        metadata = {}
        for bit in metadata_bits:
            split = bit.find("=")
            if split != -1:
                metadata[bit[:split].strip()] = json.loads(bit.strip()[split+2:-1])

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

        time.sleep(1)

    with open("airline_routes.json", "w") as f:
        f.write(json.dumps(airports, indent=4, sort_keys=True, separators=(",", ": ")))
