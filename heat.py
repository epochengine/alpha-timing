import mappers


class Heat:

    def __init__(self, heat_data: dict) -> None:
        competitors = heat_data['competitors']
        # 'scid' is the mystical ID that ties people to results
        competitors_by_scid = {c['scid']: {'name': c['na'], 'weight_class': mappers.map_weight_class(c['sc'])}
                               for c in competitors if c['laps']}
        self.results_by_competitor = {competitors_by_scid[r['scid']]['name']: int(r['fp'])
                                      for r in heat_data['results']}
        self.competitors = {c['name']: c['weight_class'] for c in competitors_by_scid.values()}

    def get_result_per_competitor(self) -> dict:
        return self.results_by_competitor

    def get_competitors(self) -> dict:
        return self.competitors
