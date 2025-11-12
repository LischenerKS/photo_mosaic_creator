import os
from typing import Optional

from PIL import Image


class InputValidator:
    """
    Класс для проверки переданных программе аргументов
    """
    def __init__(
        self,
        path_to_image_base_for_mosaic: str,
        path_to_images: str,
        path_to_output_image_dir: str,
        size_of_replaced_pixel: str,
        width_of_output_image: str,
        height_of_output_image: str,
    ):
        self.path_to_imagebase_for_mosaic = path_to_image_base_for_mosaic
        self.path_to_images = path_to_images
        self.path_to_output_image_dir = path_to_output_image_dir
        self.size_of_replaced_pixel = size_of_replaced_pixel
        self.width_of_output_image = width_of_output_image
        self.height_of_output_image = height_of_output_image

    def check_args(self) -> None:
        """
        Вызывает методы для проверки self.args
        Если аргумент(ы) некорректны, то выводит пользователю какие из аргументов некорректны
        и останавливает выполнение всей программы.
        """
        incorrect_args = [
            self._check_path_to_imagebase_for_mosaic(),
            self._check_path_to_images_dir(),
            self._check_path_to_output_image_dir(),
            self._check_size_of_replaced_pixel(),
            self._check_width_of_output_image(),
            self._check_height_of_output_image(),
        ]

        is_given_incorrect_args = False

        for inc_arg in incorrect_args:
            if inc_arg is not None:
                is_given_incorrect_args = True
                print(f"Аргумент {inc_arg} введен неверно!")

        if is_given_incorrect_args:
            print("Попробуйте еще раз.")
            exit()

    def _check_path_to_imagebase_for_mosaic(self) -> Optional[str]:
        """
        Пытается открыть указанный в self.path_to_imagebase_for_mosaic файл как изображение.
        Если файл не удалось открыть, то возвращает
        строку 'path_to_imagebase_for_mosaic'.
        Если файл удалось открыть, то возвращает None
        """
        try:
            Image.open(self.path_to_imagebase_for_mosaic).close()
            return None
        except:
            return "path_to_imagebase_for_mosaic"

    def _check_path_to_images_dir(self) -> Optional[str]:
        """
        Пытается,
        прочитать список имен по полученному из path_to_images пути
        и открыть каждое из списка как изображение.
        Если хотя бы один файл не удалось открыть, то возвращает строку 'path_to_images'.
        Если каждый файл удалось открыть, то возвращает None
        """
        try:
            image_names = os.listdir(self.path_to_images)
            for image_name in image_names:
                path = os.path.join(self.path_to_images, image_name)
                Image.open(path).close()
            return None
        except:
            return "path_to_images"

    def _check_path_to_output_image_dir(self) -> Optional[str]:
        """
        Пытается получить path_to_output_image_dir путь до директории
        для сохранения полученного изображения,
        и проверить что директория существует.
        Если директория не существует, то создает ее
        Если создать или открыть директорию не удается, то
        возвращает строку 'path_to_output_image_dir'
        """
        try:
            if not os.path.isdir(self.path_to_output_image_dir):
                os.mkdir(self.path_to_output_image_dir)
                return None
            return None
        except:
            return "path_to_output_image_dir"

    def _check_size_of_replaced_pixel(self) -> Optional[str]:
        """
        Пытается получить из size_of_replaced_pixel размер пикселя для замены
        и проверить что это целое положительное число
        Если проверка не выполняется или оказывается ложной, то возвращает строку 'size_of_replaced_pixel'.
        Иначе возвращает None
        """
        try:
            if not (int(self.size_of_replaced_pixel) > 0):
                return "size_of_replaced_pixel"
            return None
        except:
            return "size_of_replaced_pixel"

    def _check_width_of_output_image(self) -> Optional[str]:
        """
        Пытается получить из self.width_of_output_image ширину итогового изображения
        и проверить что она является целым положительным числом или None.
        Если проверка не выполняется или оказывается ложной, то возвращает строку 'width_of_output_image'.
        Иначе возвращает None
        """
        try:
            if (
                self.width_of_output_image is None
                or int(self.width_of_output_image) > 0
            ):
                return None
            else:
                return "width_of_output_image"
        except:
            return "width_of_output_image"

    def _check_height_of_output_image(self) -> Optional[str]:
        """
        Пытается получить из self.height_of_output_image высоту итогового изображения
        и проверить что она является целым положительным числом или None.
        Если проверка не выполняется или оказывается ложной, то возвращает строку 'height_of_output_image'.
        Иначе возвращает None
        """
        try:
            if (
                self.height_of_output_image is None
                or int(self.height_of_output_image) > 0
            ):
                return None
            else:
                return "height_of_output_image"
        except:
            return "height_of_output_image"
