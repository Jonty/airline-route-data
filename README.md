Global airline routes data
==========================

This is a single JSON file that describes every passenger airport and their outbound airline routes, automatically updated weekly.

The file is indexed by IATA airport code. Routes specify the destination airport IATA code, flight time in minutes, and distance in kilometers.

You probably want to look at [airline_routes.json](airline_routes.json).

Example entry
-------------
```JSON
{
    "AAN": {
        "city_name": "Al Ain",
        "continent": "AS",
        "country": "United Arab Emirates",
        "country_code": "AE",
        "display_name": "Al Ain International Airport (AAN), United Arab Emirates",
        "elevation": 869,
        "iata": "AAN",
        "icao": "OMAL",
        "latitude": "24.260231",
        "longitude": "55.616626",
        "name": "Al Ain International Airport",
        "routes": [
            {
                "carriers": [
                    "Air India Express"
                ],
                "iata": "CCJ",
                "km": 2594,
                "min": 230
            },
            {
                "carriers": [
                    "Etihad Airways"
                ],
                "iata": "JED",
                "km": 1711,
                "min": 175
            },
            {
                "carriers": [
                    "Pakistan International Airlines"
                ],
                "iata": "PEW",
                "km": 1882,
                "min": 175
            }
        ],
        "timezone": "Asia/Dubai"
    }
}
```

A nice map of the data
----------------------
<img src="https://raw.githubusercontent.com/Jonty/airline-route-data/master/map.png">
