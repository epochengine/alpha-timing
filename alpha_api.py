import mappers

from alpha_http import AlphaHttp


class AlphaApi:

    def __init__(self, http: AlphaHttp, event: int) -> None:
        self.event = event
        self.alpha_http = http

    def get_ordered_heat_results(self, heat: int) -> list:
        results = self.alpha_http.get_heat_results(self.event, heat)
        competitors = results['session']['competitors']
        placings = results['session']['results']
        # 'scid' is the mystical ID that ties people to results
        competitors_by_scid = \
            {c['scid']: {'name': c['na'], 'weight_class': mappers.map_weight_class(c['sc'])}
             for c in competitors if c['laps']}

        heat_results = list()
        placings.sort(key=lambda p: int(p['fp']))
        for i in range(len(placings)):
            competitor = competitors_by_scid[placings[i]['scid']]
            heat_results.append({
                'pos': i + 1,
                'name': competitor['name'],
                'weight_class': competitor['weight_class']
            })

        return heat_results

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
    for event_heat in event_heats:
        print(event_heat['name'])
        print(alpha_api.get_ordered_heat_results(event_heat['id']))
        print()
