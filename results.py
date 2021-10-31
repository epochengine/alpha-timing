class Results(object):

    def __init__(self) -> None:
        self.lightweights = list()
        self.middleweights = list()
        self.heavyweights = list()

    def add_result(self, pos: int, name: str, weight_class: str) -> None:
        weight_list = self.__map_class_to_list(weight_class)
        weight_list.append({'pos': pos, 'name': name})

    def __map_class_to_list(self, weight_class: str) -> list:
        if weight_class.startswith('S'):  # Silverstone
            return self.lightweights
        elif weight_class.startswith('M'):  # Monza
            return self.middleweights
        elif weight_class.startswith('F'):  # Fiji
            return self.heavyweights
        else:
            raise ValueError(f'Unknown weight class {weight_class}')

    def build_final_result(self) -> dict:
        pass

    def __build_category_result(self, weight_list: list) -> dict:
        pass
