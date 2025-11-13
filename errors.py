class ParserTypeNotExistsError(Exception):
    def __init__(self, parser_type):
        super().__init__(f"Переданный тип парсера не существует: {parser_type}")


class ClosestColorNotFoundError(Exception):
    def __init__(self, pixel):
        super().__init__(
            f"Для переданного пикселя {pixel} не удалось найти ближайший цвет в avg_colors_images"
        )
