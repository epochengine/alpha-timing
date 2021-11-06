from alpha_http import AlphaHttp

from heat import Heat
from round import Round


class AlphaApi:

    def __init__(self, http: AlphaHttp, event: int) -> None:
        self.event = event
        self.alpha_http = http

    def get_heat(self, heat_id: int) -> Heat:
        results = self.alpha_http.get_heat_results(self.event, heat_id)
        if not results['session']:
            raise ValueError("Invalid response from API")
        return Heat(results['session'])

    def get_event_heat_ids(self) -> list:
        sessions = self.alpha_http.get_event_sessions(self.event)
        # Relies on heat names being 'Heat.* <heat number>'
        heats = [{'id': s['tsid'], 'name': s['name']} for s in sessions['sessions'] if s['name'].startswith('Heat')]
        heats.sort(key=lambda s: s['name'].split(' ')[-1])
        return heats


# TODO: Move away from event_* when we can stop shadowing in method
if __name__ == '__main__':
    alpha_http = AlphaHttp('bayford', 2021)
    alpha_api = AlphaApi(alpha_http, 1597)
    event_heats = alpha_api.get_event_heat_ids()
    heat_results = [alpha_api.get_heat(heat['id']) for heat in event_heats]
    all_competitors = dict()
    for heat in heat_results:
        all_competitors.update(heat.get_competitors())

    round = Round(all_competitors, heat_results)
    print(round.get_standings())
