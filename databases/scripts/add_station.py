import argparse
import logging

import db
import openaq_client as openaq

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("add_station")


def add_by_location_id(location_id: int):
    detail = openaq.get_location(location_id)
    results = detail.get("results", [])
    if not results:
        logger.error(f"Location id {location_id} tidak ditemukan di OpenAQ.")
        return

    loc = results[0]
    station_id = db.upsert_station(
        openaq_location_id=loc["id"],
        station_name=loc.get("name", f"Location {location_id}"),
        country=loc.get("country", {}).get("name"),
        city=loc.get("locality"),
        latitude=loc.get("coordinates", {}).get("latitude"),
        longitude=loc.get("coordinates", {}).get("longitude"),
    )
    logger.info(f"Station tersimpan: db_id={station_id}, openaq_location_id={location_id}, nama={loc.get('name')}")


def search_and_list(query: str):
    result = openaq.search_locations(city=query, limit=20)
    for loc in result.get("results", []):
        print(f"id={loc['id']:<10} name={loc.get('name'):<30} city={loc.get('locality')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--location-id", type=int, help="OpenAQ location id yang mau didaftarkan")
    parser.add_argument("--search", type=str, help="Cari location berdasarkan nama kota")
    args = parser.parse_args()

    if args.location_id:
        add_by_location_id(args.location_id)
    elif args.search:
        search_and_list(args.search)
    else:
        parser.print_help()