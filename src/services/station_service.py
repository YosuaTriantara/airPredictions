from src.database.repository import repository


class StationService:

    def all(self):
        return repository.get_all_station()

    def detail(
        self,
        station_id
    ):

        return repository.get_station(
            station_id
        )


station_service = StationService()
