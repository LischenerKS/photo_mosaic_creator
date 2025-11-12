class ParserTypeNotExists(Exception):
    def __init__(self, parser_type):
        super().__init__(f"Переданный тип парсера не существует: {parser_type}")
