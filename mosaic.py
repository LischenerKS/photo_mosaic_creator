import os

from PIL import Image
from dotenv import load_dotenv
from dotenv.main import with_warn_for_invalid_lines
from tqdm import tqdm

from args_parsers import ArgsParserFabric


from environments import MODEL_KEY
from errors import ClosestColorNotFoundError
from image_loader import ImageLoader
from image_saver import ImageSaverFabric


class MosaicCreator:
    """
    класс для генерации мозаики
    """

    def __init__(self, images, images_width, images_height):
        self._images = images
        self._avg_colors_images = self._get_avg_colors_array(self._images)

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

    def _get_avg_colors_array(self, images) -> list[tuple[int, int, int]]:
        """
        метод возвращающий для self.images массив средних цветов
        """
        avg_colors = []

        for image in images:
            avg_colors.append(self._get_avg_color_image(image))

        return avg_colors

    def _get_distance_between_pixels(self, pixel_1, pixel_2) -> int:
        delta_r = abs(pixel_1[0] - pixel_2[0])
        delta_g = abs(pixel_1[1] - pixel_2[1])
        delta_b = abs(pixel_1[2] - pixel_2[2])
        return delta_r + delta_b + delta_g

    def _find_index_of_closest_by_avg_color_image(
        self, pixel, avg_colors_images
    ) -> int:
        """
        находит в avg_colors_images ближайшее по среднему цвету изображение
        к переданному pixel и возвращает его index
        """

        min_delta = 10**10
        result_id = -1

        for i in range(len(avg_colors_images)):
            distance = self._get_distance_between_pixels(pixel, avg_colors_images[i])

            if distance < min_delta:
                min_delta = distance
                result_id = i

        if result_id == -1:
            raise ClosestColorNotFoundError(pixel)

        return result_id

    def create_and_show_mosaic_image(self, old_image) -> Image:
        """
        создает изображение new_image где пиксели в old_image заменены
        на ближайшие по среднему цвету изображения из images
        и возвращает его
        """

        new_image_pixels = []
        """
        для i-го пикселя старого изображения хранит id
        ближайшего по среднему цвету изображения в _images
        """

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
                    pixel, self._avg_colors_images
                )
                new_image_pixels.append(closest_image_ids)

        new_image = Image.new("RGB", (new_image_width, new_image_height))

        image_id = 0
        for h in tqdm(
            range(old_image.height),
            desc="Создаем новое изображение",
            leave=False,
            colour="green",
        ):
            for w in range(old_image.width):
                new_w = w * self._images_width
                new_h = h * self._images_height
                image_to_replace_pixel = self._images[new_image_pixels[image_id]]
                new_image.paste(image_to_replace_pixel, (new_w, new_h))
                image_id += 1

        return new_image


class MosaicFacade:
    def create_mosaic(self, args_sourse: str) -> None:
        parser_fabric = ArgsParserFabric()
        argparser = parser_fabric.get_parser(args_sourse)

        args = argparser.get_args_dictionary()

        image_loader = ImageLoader(args["path_to_images"])

        path_to_imagebase_for_mosaic = args["path_to_imagebase_for_mosaic"]
        base_image = image_loader.get_image_by_path(path_to_imagebase_for_mosaic)

        if args["width_of_output_image"] is None:
            args["width_of_output_image"] = (
                MODEL_KEY["DEFAULT_SCALE_MULTIPLIER"] * base_image.width
            )

        if args["height_of_output_image"] is None:
            args["height_of_output_image"] = (
                MODEL_KEY["DEFAULT_SCALE_MULTIPLIER"] * base_image.height
            )

        base_image = base_image.resize(
            (args["width_of_output_image"], args["height_of_output_image"])
        )

        images_with_names = image_loader.get_images_with_names()

        width_of_replaced_pixel = args["size_of_replaced_pixel"]
        height_of_replaced_pixel = args["size_of_replaced_pixel"]

        image_loader.resize_images(
            images_with_names[1], width_of_replaced_pixel, height_of_replaced_pixel
        )

        my_mosaic_creator = MosaicCreator(
            images_with_names[1],
            width_of_replaced_pixel,
            height_of_replaced_pixel,
        )

        output_image = my_mosaic_creator.create_and_show_mosaic_image(base_image)

        my_image_saver_fabric = ImageSaverFabric()
        my_image_saver = my_image_saver_fabric.get_input_saver(
            input_save_type="dir", path_to_output_image=args["path_to_output_image_dir"]
        )
        print(
            f"Генерация успешно завершена, путь до изображения {my_image_saver.save(output_image)}"
        )
