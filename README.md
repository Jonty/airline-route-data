Global airline routes data
==========================

This is a single JSON file that describes every passenger airport and their outbound airline routes, automatically updated weekly.

The file is indexed by IATA airport code. Routes specify the destination airport IATA code, flight time in minutes, and distance in kilometers.

You probably want to look at [airline_routes.json](airline_routes.json).

A nice map of the data
----------------------
<img src="https://raw.githubusercontent.com/Jonty/airline-route-data/master/map.png">

Example entry
-------------
```JSON
{
    "LHR": {
        "city_name": "London",
        "continent": "EU",
        "country": "United Kingdom",
        "country_code": "GB",
        "display_name": "London (LHR), United Kingdom",
        "elevation": 80,
        "iata": "LHR",
        "icao": "EGLL",
        "latitude": "51.469603",
        "longitude": "-0.453566",
        "name": "Heathrow",
        "routes": [
            {
                "carriers": [
                    {
                        "iata": "BA",
                        "name": "British Airways"
                    },
                    {
                        "iata": "KL",
                        "name": "KLM"
                    }
                ],
                "iata": "AMS",
                "km": 371,
                "min": 80
            },
            {
                "carriers": [
                    {
                        "iata": "BA",
                        "name": "British Airways"
                    },
                    {
                        "iata": "LH",
                        "name": "Lufthansa"
                    }
                ],
                "iata": "MUC",
                "km": 943,
                "min": 115
            },
            {
                "carriers": [
                    {
                        "iata": "AF",
                        "name": "Air France"
                    },
                    {
                        "iata": "BA",
                        "name": "British Airways"
                    }
                ],
                "iata": "CDG",
                "km": 348,
                "min": 80
            },
            ...
        ],
        "timezone": "Europe/London"
    }
}
```
