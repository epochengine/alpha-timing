import itertools

from heat import Heat


class Round:

    def __init__(self, competitors: dict, heats: list[Heat]) -> None:
        self.competitors = competitors
        self.results_per_competitor = self.__build_results_per_competitor(competitors, heats)

    def get_standings(self) -> dict:
        round_standings = dict()
        for competitor in self.results_per_competitor:
            points = 0
            # TODO: try a reduce
            for heat_result in self.results_per_competitor[competitor]:
                points += self.__points_for_heat_position(heat_result)
            round_standings[competitor] = {'points': points,
                                           'ordered_results': sorted(self.results_per_competitor[competitor])}

        tie_broken_round_standings = self.__tie_break_standings(round_standings)
        light_result = self.__build_result_for_weight_class(tie_broken_round_standings, 'LIGHT')
        middle_result = self.__build_result_for_weight_class(tie_broken_round_standings, 'MIDDLE')
        heavy_result = self.__build_result_for_weight_class(tie_broken_round_standings, 'HEAVY')
        return {'LIGHT': light_result, 'MIDDLE': middle_result, 'HEAVY': heavy_result}

    @staticmethod
    def __tie_break_standings(round_standings: dict) -> list:
        competitor_points_buckets = dict()
        for competitor, standing in round_standings.items():
            points = standing['points']
            bucket = list()
            if points in competitor_points_buckets:
                bucket = competitor_points_buckets[points]
            bucket.append({'competitor': competitor, 'results': standing['ordered_results']})
            competitor_points_buckets[points] = bucket

        for points, bucket in competitor_points_buckets.items():
            competitor_points_buckets[points] = sorted(bucket, key=lambda c: c['results'])
        tie_broken_standings = []
        for (_, bucket) in sorted(competitor_points_buckets.items(), reverse=True):
            tie_broken_standings.append([b['competitor'] for b in bucket])
        return list(itertools.chain.from_iterable(tie_broken_standings))

    def __build_result_for_weight_class(self, round_standings: list, weight_class: str) -> dict:
        result_split = [competitor for competitor in round_standings if self.competitors[competitor] == weight_class]

        result = dict()
        for i in range(len(result_split)):
            pos = i + 1
            result[pos] = {'name': result_split[i], 'points': self.__points_for_round_position(pos)}

        return result

    @staticmethod
    def __build_results_per_competitor(competitors: dict, heats: list[Heat]) -> dict:
        results = {c: list() for c in competitors.keys()}
        for heat in heats:
            competitor_results = heat.get_result_per_competitor()
            for competitor in competitor_results:
                results[competitor].append(competitor_results[competitor])
        return results

    # TODO: Put these two as implementations of a simple ABC
    @staticmethod
    def __points_for_heat_position(pos: int) -> int:
        if pos == 1:
            return 25
        elif pos <= 24:
            return 25 - pos
        else:
            return 0

    @staticmethod
    def __points_for_round_position(pos: int) -> int:
        if pos == 1:
            return 50
        elif pos <= 24:
            return 45 - ((pos - 2) * 2)
        return 0
