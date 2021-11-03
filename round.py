class Round:

    # def __init__(self, competitors: dict, heat_results: list[dict]) -> None:
    def __init__(self, heat_results: list[dict]) -> None:
        self.heat_results = heat_results

    def standings_in_overall_order(self) -> dict:
        round_standings = dict()
        for heat in self.heat_results:
            if not isinstance(heat, list):
                raise TypeError(f'Invalid heat result of type {type(heat)}')
            for result in heat:
                if not result['pos'] or not result['name']:
                    raise ValueError('Incorrectly constructed result')

                competitor = result['name']
                points_so_far = 0
                if competitor in round_standings:
                    points_so_far = round_standings.get(competitor)['points']
                points_so_far += self.points_for_heat_position(result['pos'])
                round_standings[competitor] = {'points': points_so_far, 'weight_class': result['weight_class']}

        # TODO: This naming and structure is awful.
        light_result = self.build_result_for_weight_class(round_standings, 'LIGHT')
        middle_result = self.build_result_for_weight_class(round_standings, 'MIDDLE')
        heavy_result = self.build_result_for_weight_class(round_standings, 'HEAVY')
        return {'LIGHT': light_result, 'MIDDLE': middle_result, 'HEAVY': heavy_result}

    def build_result_for_weight_class(self, round_standings: dict, weight_class: str) -> dict:
        # TODO: Tie breaks
        result_split = [competitor for competitor, points in
                        sorted(round_standings.items(), key=lambda standing: standing[1]['points'], reverse=True)
                        if points['weight_class'] == weight_class]

        result = dict()
        for i in range(len(result_split)):
            pos = i + 1
            result[pos] = {'name': result_split[i], 'points': self.points_for_round_position(pos)}

        return result

    @staticmethod
    def points_for_heat_position(pos: int) -> int:
        if pos == 1:
            return 25
        elif pos <= 24:
            return 25 - pos
        else:
            return 0

    @staticmethod
    def points_for_round_position(pos: int) -> int:
        if pos == 1:
            return 50
        elif pos <= 24:
            return 45 - ((pos - 2) * 2)
        return 0

    # @staticmethod
    # def split_into_weight_classes(heat_results: list[dict]) -> dict:
    #     light_pos, middle_pos, heavy_pos = 1, 1, 1
    #     light_split, middle_split, heavy_split = dict(), dict(), dict()
    #     for heat_result in heat_results:
    #         if not isinstance(heat_result, list):
    #             raise TypeError(f'Invalid heat result of type {type(heat_result)}')
    #         for results in heat_result:
    #             for result in results:
    #                 if not result['pos'] or not result['name']:
    #                     raise ValueError('Incorrectly constructed result')
    #                 if result['weight_class'] == 'LIGHT':
    #                     light_split[light_pos] = result['name']
    #                     light_pos += 1
    #                 elif result['weight_class'] == 'MIDDLE':
    #                     middle_split[middle_pos] = result['name']
    #                     middle_pos += 1
    #                 else:
    #                     heavy_split[heavy_pos] = result['name']
    #                     heavy_pos += 1
    #     return {'LIGHT': light_split, 'MIDDLE': middle_split, 'HEAVY': heavy_split}
