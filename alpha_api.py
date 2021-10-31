from alpha_http import AlphaHttp


class AlphaApi:

    def __init__(self, event: int) -> None:
        self.event = event

    def get_ordered_heat_results(self) -> list:
        http = AlphaHttp('bayford', 2021)
        results = http.get_heat_results(self.event, 4438)  # TODO
        competitors = results['session']['competitors']
        placings = results['session']['results']
        # 'scid' is the mystical ID that ties people to results
        competitors_by_scid = \
            {c['scid']: {'name': c['na'], 'weight_class': self.map_weight_class(c['sc'])} for c in competitors}

        heat_results = list()
        placings.sort(key=lambda p: int(p['fp']))
        for placing in placings:
            heat_results.append(competitors_by_scid[placing['scid']])

        return heat_results

    @staticmethod
    def map_weight_class(weight_class: str) -> str:
        if weight_class.startswith('Silverstone'):
            return 'LIGHT'
        elif weight_class.startswith('Monza'):
            return 'MIDDLE'
        elif weight_class.startswith('Fiji'):
            return 'HEAVY'
        else:
            raise ValueError(f'Unknown weight class {weight_class}')


if __name__ == '__main__':
    alpha_api = AlphaApi(1597)
    print(alpha_api.get_ordered_heat_results())
