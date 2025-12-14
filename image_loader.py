import os

from PIL import Image
from tqdm import tqdm


class ImageLoader:
    """
    класс содержит утилиты для загрузки изображений из указанной папки
    """

    def __init__(self, path_to_images):
        self._PATH_TO_IMAGES = path_to_images

    def resize_images(self, images, width, height) -> None:
        for i in tqdm(
            range(len(images)),
            desc="Сжимаем изображения для замены",
            leave=False,
            colour="yellow",
        ):
            images[i] = images[i].resize((width, height))

    def get_images_with_names(self) -> tuple[list[str], list[Image]]:
        images = ([], [])
        image_names = os.listdir(self._PATH_TO_IMAGES)

        for image_name in tqdm(
            image_names, desc="Открываем изображения", leave=False, colour="cyan"
        ):
            path_to_image = os.path.join(self._PATH_TO_IMAGES, image_name)
            with Image.open(path_to_image) as img:
                img.load()
                images[0].append(image_name)
                images[1].append(img)

        return images

    def get_image_by_path(self, path) -> Image:
        """
        Возвращает Image по переданному пути
        Путь должен быть корректным
        """

        with Image.open(path) as img:
            img.load()
            image = img

        return image
