def map_weight_class(weight_class: str) -> str:
    if weight_class.startswith('Silverstone'):
        return 'LIGHT'
    elif weight_class.startswith('Monza'):
        return 'MIDDLE'
    elif weight_class.startswith('Fiji'):
        return 'HEAVY'
    else:
        raise ValueError(f'Unknown weight class {weight_class}')
