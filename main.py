from PIL import Image
import os

class _ImageLoader:
    #*содержит утилиты для загрузки изображений из указанной папки
    #todo сделать проверку корректности пути и метод для его изменения 
    _PATH_TO_IMAGES = './images/'

    @classmethod
    def get_images(cls) -> list[Image]:
        images = []
        image_names = os.listdir(cls._PATH_TO_IMAGES)

        for image_name in image_names:
            path_to_image = f'{cls._PATH_TO_IMAGES}{image_name}'

            with Image.open(path_to_image) as img:
                img.load()
                images.append(img)
        return images


class MosaicGenerator:
    #*класс для генерации мозайки
    pass