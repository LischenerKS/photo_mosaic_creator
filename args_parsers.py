import argparse
import os
from abc import ABC, abstractmethod

import input_validator
from environments import MODEL_KEY
from errors import ParserTypeNotExistsError


class ArgsParserFabric:
    """
    Класс для создания объектов разных классов парсера аргументов
    """

    def get_parser(self, parser_type):
        if parser_type == "cli":
            return CLIArgsParser()
        elif parser_type == "another":
            return AnotherArgsParser()
        else:
            raise ParserTypeNotExistsError(parser_type)


class AbstractArgsParser(ABC):
    """
    Абстрактный класс парсера аргументов
    """

    def __init__(self):
        self._args_dictionary = self._get_args()

    @abstractmethod
    def _get_args(self) -> dict:
        """
        Абстрактный метод для парсинга аргументов
        """

        pass

    def get_args_dictionary(self) -> dict:
        """
        Метод, возвращающий словарь аргументов
        """
        return self._args_dictionary

    def calculate_output_image_size(self, orig_w: int, orig_h: int) -> dict:
        args_with_new_image_size = self._args_dictionary.copy()

        if (args_with_new_image_size["width_of_output_image"] is None) and (
            args_with_new_image_size["height_of_output_image"] is None
        ):
            args_with_new_image_size["width_of_output_image"] = (
                orig_w * MODEL_KEY["DEFAULT_SCALE_MULTIPLIER"]
            )
            args_with_new_image_size["height_of_output_image"] = (
                orig_h * MODEL_KEY["DEFAULT_SCALE_MULTIPLIER"]
            )

        elif args_with_new_image_size["width_of_output_image"] is None:
            args_with_new_image_size["width_of_output_image"] = (
                orig_w * args_with_new_image_size["height_of_output_image"]
            ) // orig_h

        elif args_with_new_image_size["height_of_output_image"] is None:
            args_with_new_image_size["height_of_output_image"] = (
                orig_h * args_with_new_image_size["width_of_output_image"]
            ) // orig_w

        else:
            pass

        return args_with_new_image_size


class AnotherArgsParser(AbstractArgsParser):
    """
    Нереализованный класс парсера аргументов.
    Нужен чтобы использование паттерна фабрика
    не выглядело бесполезным.
    """

    def get_args(self):
        return dict()  #!не реализовано


class CLIArgsParser(AbstractArgsParser):
    """
    Класс для парсинга аргументов из командной строки
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Строит мозаику по выбранным изображениям", exit_on_error=False
        )

        self.parser.add_argument(
            "path_to_imagebase_for_mosaic",
            type=str,
            help="Путь до изображения, по которому строится мозаика",
        )

        self.parser.add_argument(
            "-indir",
            "--path_to_images",
            type=str,
            help="Путь до директории, в которой находятся \
                            изображения, которые будут заменять пиксели.",
            required=True,
        )

        self.parser.add_argument(
            "-outdir",
            "--path_to_output_image_dir",
            type=str,
            help="Путь до директории, в которой \
                            сохранится результат работы программы.",
            required=True,
        )

        self.parser.add_argument(
            "-srp",
            "--size_of_replaced_pixel",
            type=int,
            help="размер изображения, которое будет \
                            заменять пиксель",
            default=MODEL_KEY["DEFAULT_SIZE_OF_REPLACED_PIXEL"],
            required=False,
        )

        self.parser.add_argument(
            "-woi",
            "--width_of_output_image",
            type=int,
            help="ширина полученного изображения в \
                                 замененных пикселях",
            required=False,
        )

        self.parser.add_argument(
            "-hoi",
            "--height_of_output_image",
            type=int,
            help="высота полученного изображения в \
                                 замененных пикселях",
            required=False,
        )

        self.parser.add_argument(
            "-?", "--show_help", action="help", help="Показать справку"
        )

        self._args_dictionary = self._get_args()

    def _get_args(self) -> dict:
        """
        Метод для парсинга аргументов командной строки в словарь
        """
        try:
            args = self.parser.parse_args()

            args_dictionary = dict()
            args_dictionary["path_to_imagebase_for_mosaic"] = (
                args.path_to_imagebase_for_mosaic
            )
            args_dictionary["path_to_images"] = args.path_to_images
            args_dictionary["path_to_output_image_dir"] = args.path_to_output_image_dir
            args_dictionary["size_of_replaced_pixel"] = args.size_of_replaced_pixel
            args_dictionary["width_of_output_image"] = args.width_of_output_image
            args_dictionary["height_of_output_image"] = args.height_of_output_image

            cur_input_validator = input_validator.InputValidator(
                path_to_image_base_for_mosaic=args.path_to_imagebase_for_mosaic,
                path_to_images=args.path_to_images,
                path_to_output_image_dir=args.path_to_output_image_dir,
                size_of_replaced_pixel=args.size_of_replaced_pixel,
                width_of_output_image=args.width_of_output_image,
                height_of_output_image=args.height_of_output_image,
            )
            cur_input_validator.check_args()

            self.args_dictionary = args_dictionary
            return args_dictionary

        except argparse.ArgumentError:
            print("Ошибка в аргументах, попробуйте еще раз.\n")
            self.parser.print_help()
            exit()
