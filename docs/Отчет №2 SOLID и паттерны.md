### Паттерны:
#### Фабрика
https://github.com/LischenerKS/photo_mosaic_creator/blob/7f34f8913a01d68a49c792a06d8cfda1a7bcf038/main.py#L132-L142
Если мы решим добавить другой способ сбора аргументов для запуска (например брать их из какого-нибудь config`а, то будет достаточно прописать конкретную реализацию класса AnotherArgsParser и поменять одну строчку в ArgsParserFabric
#### Фасад
https://github.com/LischenerKS/photo_mosaic_creator/blob/7f34f8913a01d68a49c792a06d8cfda1a7bcf038/main.py#L412-L451
Достаточно указать откуда взять аргументы и мозаика будет сгенерирована
Скрывает внутреннюю работу с другими классами и вместо нее предоставляет простой и понятный инструмент для работы со сложной системой

### SOLID:
#### S
Каждый класс в файле отвечает за что-то свое
#### O
https://github.com/LischenerKS/photo_mosaic_creator/blob/7f34f8913a01d68a49c792a06d8cfda1a7bcf038/main.py#L144-L179
Можно легко добавить новый источник аргументов без значительного изменения логики
#### L
https://github.com/LischenerKS/photo_mosaic_creator/blob/7f34f8913a01d68a49c792a06d8cfda1a7bcf038/main.py#L144-L179
#### I
https://github.com/LischenerKS/photo_mosaic_creator/blob/7f34f8913a01d68a49c792a06d8cfda1a7bcf038/main.py#L144-L179
Не содержит лишних методов, которые использует только конкретный наследник
#### D
MosaicFacade напрямую не зависит от конкретной реализации парсера, так как он получается через фабричный метод