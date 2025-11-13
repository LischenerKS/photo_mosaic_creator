import os
from abc import ABC, abstractmethod

from PIL import Image
from errors import UnrealizedImageSaverInvokedError


class ImageSaverFabric:
    """
    Класс для создания объектов разных классов Сохранителя изображений
    """

    def get_input_saver(self, input_save_type: str, path_to_output_image: str):
        if input_save_type == "dir":
            return DirectoryImageSaver(path_to_output_image_dir=path_to_output_image)
        elif input_save_type == "another":
            return AnotherImageSaver()
        else:
            raise UnrealizedImageSaverInvokedError(input_save_type)


class AbstractImageSaver(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _get_free_path_to_image(self):
        pass

    @abstractmethod
    def save(self, image: Image):
        pass


class DirectoryImageSaver(AbstractImageSaver):
    """
    Сохраняет передаваемые изображения в переданную в конструктор директорию
    """

    def __init__(self, path_to_output_image_dir):
        self._path_to_output_image_dir = path_to_output_image_dir

    def _get_free_path_to_image(self) -> str:
        output_image_counter = 0
        free_path_to_image = os.path.join(
            self._path_to_output_image_dir, f"output_image_{output_image_counter}.jpg"
        )
        while os.path.exists(free_path_to_image):
            output_image_counter += 1
            free_path_to_image = os.path.join(
                self._path_to_output_image_dir,
                f"output_image_{output_image_counter}.jpg",
            )
        return free_path_to_image

    def save(self, image: Image) -> str:
        free_path_to_image = self._get_free_path_to_image()
        image.save(free_path_to_image)
        return free_path_to_image


class AnotherImageSaver(AbstractImageSaver):
    """
    Нереализованный альтернативный класс для сохранения изображений
    """

    def _get_free_path_to_image(self):
        pass

    def save(self, image: Image):
        pass
