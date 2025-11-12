import os

from PIL import Image
from dotenv import load_dotenv
from tqdm import tqdm

from args_parsers import ArgsParserFabric


class ImageLoader:
    """
    класс содержит утилиты для загрузки изображений из указанной папки
    путь переданный в конструктор должен быть корректным
    """

    def __init__(self, path_to_images):
        self._PATH_TO_IMAGES = path_to_images

    def resize_base_image(self, orig_image, mosaic_size, pixel_size) -> Image:
        """
        Приводит изображение, по которому строится мозаика, к такому
        размеру, чтобы при заданном pixel_size получился ожидаемый
        mosaic_size.
        """
        mosaic_width = mosaic_size[0]
        mosaic_height = mosaic_size[1]

        pixel_width = pixel_size[0]
        pixel_height = pixel_size[1]

        new_orig_image_width = mosaic_width // pixel_width
        new_orig_image_height = mosaic_height // pixel_height

        orig_image = orig_image.resize((new_orig_image_width, new_orig_image_height))

        return orig_image

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


class MosaicCreator:
    """
    класс для генерации мозаики
    """

    def __init__(self, images, images_width, images_height, path_to_output_image):
        self._images = images
        self._avg_colors_images = self._get_avg_colors_array()

        self._path_to_output_image = path_to_output_image

        self._images_width = images_width
        self._images_height = images_height

    def _get_avg_color_image(self, image) -> tuple[int, int, int]:
        """
        метод возвращающий для изображения его средний цвет
        """
        r = 0
        g = 0
        b = 0
        count_pixels = image.width * image.height

        for width in range(image.width):
            for height in range(image.height):
                pixel = image.getpixel((width, height))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]

        r //= count_pixels
        g //= count_pixels
        b //= count_pixels

        return r, g, b

    def _get_avg_colors_array(self) -> list[tuple[int, int, int]]:
        """
        метод возвращающий для self.images массив средних цветов
        """
        avg_colors = []

        for image in self._images:
            avg_colors.append(self._get_avg_color_image(image))

        return avg_colors

    def _get_distance_between_pixels(self, pixel_1, pixel_2) -> int:
        delta_r = abs(pixel_1[0] - pixel_2[0])
        delta_g = abs(pixel_1[1] - pixel_2[1])
        delta_b = abs(pixel_1[2] - pixel_2[2])
        return delta_r + delta_b + delta_g

    def _find_index_of_closest_by_avg_color_image(self, pixel) -> int:
        """
        находит в self.avg_colors_images ближайшее по среднему цвету изображение
        к переданному pixel и возвращает его index
        """

        min_delta = 10**10
        result_id = -1

        for i in range(len(self._avg_colors_images)):
            distance = self._get_distance_between_pixels(
                pixel, self._avg_colors_images[i]
            )

            if distance < min_delta:
                min_delta = distance
                result_id = i

        if result_id == -1:
            raise Exception

        return result_id

    def create_and_show_mosaic_image(self, old_image) -> str:
        """
        создает изображение new_image где пиксели в old_image заменены
        на ближайшие по среднему цвету изображения из images
        возравращает путь до него
        """

        new_image_pixels = []
        new_image_width = old_image.width * self._images_width
        new_image_height = old_image.height * self._images_height

        for h in tqdm(
            range(old_image.height),
            desc="Готовим изображения для замены пикселей",
            leave=False,
            colour="MAGENTA",
        ):
            for w in range(old_image.width):
                pixel = old_image.getpixel((w, h))
                closest_image_ids = self._find_index_of_closest_by_avg_color_image(
                    pixel
                )
                new_image_pixels.append(closest_image_ids)

        new_image = Image.new("RGB", (new_image_width, new_image_height))

        i = 0
        for h in tqdm(
            range(old_image.height),
            desc="Создаем новое изображение",
            leave=False,
            colour="green",
        ):
            for w in range(old_image.width):
                new_w = w * self._images_width
                new_h = h * self._images_height
                image_to_replace_pixel = self._images[new_image_pixels[i]]
                new_image.paste(image_to_replace_pixel, (new_w, new_h))
                i += 1

        output_image_counter = 0
        output_image_name = os.path.join(
            self._path_to_output_image, f"output_image_{output_image_counter}.jpg"
        )
        while os.path.exists(output_image_name):
            output_image_counter += 1
            output_image_name = os.path.join(
                self._path_to_output_image, f"output_image_{output_image_counter}.jpg"
            )

        new_image.save(output_image_name)
        return output_image_name


class MosaicFacade:
    def create_mosaic(self, args_sourse: str) -> None:
        load_dotenv()

        parser_fabric = ArgsParserFabric()
        argparser = parser_fabric.get_parser(args_sourse)

        args_without_new_image_size = argparser.get_args()

        image_loader = ImageLoader(args_without_new_image_size["path_to_images"])
        images_with_names = image_loader.get_images_with_names()

        path_to_imagebase_for_mosaic = args_without_new_image_size[
            "path_to_imagebase_for_mosaic"
        ]
        base_image = image_loader.get_image_by_path(path_to_imagebase_for_mosaic)

        args = argparser.calculate_output_image_size(
            base_image.width, base_image.height
        )

        width_of_replaced_pixel = args["size_of_replaced_pixel"]
        height_of_replaced_pixel = args["size_of_replaced_pixel"]
        image_loader.resize_images(
            images_with_names[1], width_of_replaced_pixel, height_of_replaced_pixel
        )

        my_mosaic_creator = MosaicCreator(
            images_with_names[1],
            width_of_replaced_pixel,
            height_of_replaced_pixel,
            args["path_to_output_image_dir"],
        )

        mosaic_size = args["width_of_output_image"], args["height_of_output_image"]

        base_image = image_loader.resize_base_image(
            base_image, mosaic_size, (width_of_replaced_pixel, height_of_replaced_pixel)
        )

        path_to_output_image = my_mosaic_creator.create_and_show_mosaic_image(
            base_image
        )
        print(
            f"Генерация успешно завершена, путь до изображения {path_to_output_image}"
        )
