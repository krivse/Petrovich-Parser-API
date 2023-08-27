from typing import Optional

from errors import bad_request


def validation(args) -> Optional[tuple[str, str, str, str]]:
    """Call features to check incoming data."""
    _check_arguments(args)
    validate_data = _check_arguments_values(args)
    return validate_data


def _check_arguments(args) -> None:
    """Checking on missing arguments and checking the matching of the transmitted data type."""
    for i in ["type_room", "length", "width", "height"]:
        if i not in args:
            bad_request(f'Пропущено обязательное поле: {i}')
        elif not isinstance(args.get(i), str):
            bad_request(f'Значение аргумента "{i}\" должен являться строкой. Вы передали: {type(args.get(i))}')


def _check_arguments_values(value) -> Optional[tuple[str, str, str, str]]:
    """Checking for matching the transferred values."""
    LIST_ROOM = [
        'Кухня', 'Комната', 'Гостиная',
        'Санузел', 'Кухня-гостиная',
        'Прихожая', 'Спальная', 'Детская',
        'Ванная', 'Туалет', 'Гардеробная'
    ]
    MAX_HEIGHT = 9.3

    type_room = value.get('type_room')
    length = value.get('length')
    width = value.get('width')
    height = value.get('height')

    if type_room not in LIST_ROOM:
        bad_request(f'Неправильно передан тип (наименование) помещения. '
                    f'"{type_room}\" такого наименования нет в списке возможных.')
    if float(height) > MAX_HEIGHT:
        bad_request(f'Высота может быть не более 9.3 метров. Вы передали: {height} ')
    for i in [length, width, height]:
        if not i.isdigit() and not i.replace(".", "", 1).isdigit() and not i.replace(",", "", 1).isdigit():
            bad_request(f'Значение должно состоять только из числовых символов и не может содержать другие символы. '
                        f'Вы передали: {i} ')
    return type_room, length, width, height
