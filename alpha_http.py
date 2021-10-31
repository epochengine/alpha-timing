import requests


class AlphaHttp:

    def __init__(self, location: str, year: int) -> None:
        self.base_uri = f'https://results.alphatiming.co.uk/api/v1/{location}/{year}'

    def get_event_sessions(self, event: int) -> dict:
        return self.__get_json_object(f'{event}/sessions')

    def get_heat_results(self, event: int, heat: int) -> dict:
        return self.__get_json_object(f'{event}/sessions/{heat}')

    def __get_json_object(self, url_suffix: str) -> dict:
        raw = requests.get(f'{self.base_uri}/{url_suffix}')
        raw.raise_for_status()
        return raw.json()
