from PIL import Image
import os
from abc import ABC, abstractmethod
import argparse

class InputValidator:

    def __init__(self, args: dict):
        self.args = args
        self.incorrect_args = []

    def check_args(self) -> None:
        """
        Вызывает методы для проверки self.args
        Если аргумент(ы) некорректны, то выводит пользователю какие из аргументов некорректны
        и останавливает выполнение всей программы.
        """

        self.check_path_to_imagebase_for_mosaic_correct()
        self.check_path_to_images_correct()
        self.check_path_to_output_image_dir()
        self.check_size_of_replaced_pixel()
        self.check_width_of_output_image()
        self.check_height_of_output_image()

        if self.incorrect_args != []:
            for inc_arg in self.incorrect_args:
                print(f'Аргумент {inc_arg} введен неверно!')
            print('Попробуйте еще раз.')
            exit()

    def check_path_to_imagebase_for_mosaic_correct(self) -> None:
        """
        Пытается получить из self.args path_to_imagebase_for_mosaic
        и открыть указанный файл как изображение. 
        Если файл не удалось открыть, то добавляет в self.incorrect_args
        строку 'path_to_imagebase_for_mosaic'.
        Если файл удалось открыть, то ничего не делает.
        """
        try:
            path_to_imagebase_for_mosaic = self.args['path_to_imagebase_for_mosaic']
            Image.open(path_to_imagebase_for_mosaic).close()
        except:
            self.incorrect_args.append('path_to_imagebase_for_mosaic')
 
    def check_path_to_images_correct(self) -> None:
        """
        Пытается получить из self.args path_to_images_dir,
        прочитать список имен по полученному пути
        и открыть каждое из списка как изображение.
        Если хотя бы один файл не удалось открыть, то добавляет 
        в self.incorrect_args строку 'path_to_images_dir'.
        Если каждый файл удалось открыть, то ничего не делает.
        """
        try:
            path_to_images_dir = self.args['path_to_images']
            image_names = os.listdir(path_to_images_dir)
            for image_name in image_names:
                Image.open(f'{path_to_images_dir}{image_name}').close()
        except:
            self.incorrect_args.append('path_to_images_dir')
        
    def check_path_to_output_image_dir(self) -> None:
            """
            Пытается получить из self.args path_to_output_image_dir,
            и проверить что директория существует.
            Если получить аргумент не удалось или директории не существует,
            то добавляет в self.incorrect_args строку 'path_to_output_image_dir'.
            Иначе ничего не делает.
            """
            #todo добавить проверку на права для директории
            #todo добавить проверку на то что строка оканчивается на /
            try:
                path_to_output_image_dir = self.args['path_to_output_image_dir']
                if not os.path.isdir(path_to_output_image_dir):
                    self.incorrect_args.append('path_to_output_image_dir')
            except:
                self.incorrect_args.append('path_to_output_image_dir')

    def check_size_of_replaced_pixel(self) -> None:
        """
        Пытается получить из self.args size_of_replaced_pixel
        и проверить что это целое положительное число
        Если проверка не выполняется или оказывается ложной, то добавляет
        в self.incorrect_args строку 'size_of_replaced_pixel'.
        Иначе ничего не делает.
        """
        try:
            size_of_replaced_pixel = self.args['size_of_replaced_pixel']
            if not (int(size_of_replaced_pixel) > 0):
                self.incorrect_args.append('size_of_replaced_pixel')
        except:
            self.incorrect_args.append('size_of_replaced_pixel')

    def check_width_of_output_image(self) -> None:
        """
        Пытается получить из self.args 
        width_of_output_image и проверить что он является целым положительным числом или None
        Если проверка не выполняется или оказывается ложной, то добавляет
        в self.incorrect_args строку 'width_of_output_image'.
        Иначе ничего не делает.
        """
        try:
            width_of_output_image = self.args['width_of_output_image']
            if width_of_output_image is None or int(width_of_output_image) > 0:
                pass #correct
            else:
                self.incorrect_args.append('width_of_output_image')
        except:
            self.incorrect_args.append('width_of_output_image') 

    def check_height_of_output_image(self) -> None:
        """
        Пытается получить из self.args 
        height_of_output_image и проверить что он является целым положительным числом или None
        Если проверка не выполняется или оказывается ложной, то добавляет
        в self.incorrect_args строку 'height_of_output_image'.
        Иначе ничего не делает.
        """
        try:
            height_of_output_image = self.args['height_of_output_image']
            if height_of_output_image is None or int(height_of_output_image) > 0:
                pass #correct
            else:
                self.incorrect_args.append('height_of_output_image')
        except:
            self.incorrect_args.append('height_of_output_image')

class ArgsParser(ABC):
    """
    Абстрактный класс парсера аргументов 
    """
    @abstractmethod
    def get_args(self) -> dict:
        pass

class CLIArgsParser(ArgsParser):
    """
    Класс для парсинга аргументов из командной строки
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Строит мозаику по выбранным изображениям', exit_on_error=False)

        self.parser.add_argument('path_to_imagebase_for_mosaic', type=str,\
                            help='Путь до изображения, по которому строится мозаика')
        
        self.parser.add_argument('-indir', '--path_to_images', type=str, help='Путь до директории, в которой находятся \
                            изображения, которые будут заменять пиксели. Должен оканчиваться на /', required=True)
        
        self.parser.add_argument('-outdir', '--path_to_output_image_dir', type=str, help='Путь до директории, в которой \
                            сохранится результат работы программы. Должен оканчиваться на /', required=True)
        
        self.parser.add_argument('-srp', '--size_of_replaced_pixel', type=int, help='размер изображения, которое будет \
                            заменять пиксель', default=50, required=False)
        
        self.parser.add_argument('-woi', '--width_of_output_image', type=int, help='ширина полученного изображения в \
                                 замененных пикселях', required=False)
        
        self.parser.add_argument('-hoi', '--height_of_output_image', type=int, help='высота полученного изображения в \
                                 замененных пикселях', required=False)
        
        self.parser.add_argument('-?', '--show_help', action='help', help='Показать справку')
    
    def get_args(self) -> dict:
        try:        
            args = self.parser.parse_args()
            
            args_dictionary = dict()
            args_dictionary['path_to_imagebase_for_mosaic'] = args.path_to_imagebase_for_mosaic
            args_dictionary['path_to_images'] = args.path_to_images
            args_dictionary['path_to_output_image_dir'] = args.path_to_output_image_dir
            args_dictionary['size_of_replaced_pixel'] = args.size_of_replaced_pixel
            args_dictionary['width_of_output_image'] = args.width_of_output_image
            args_dictionary['height_of_output_image'] = args.height_of_output_image
            
            cur_input_validator = InputValidator(args=args_dictionary)
            cur_input_validator.check_args()
            
            return args_dictionary

        except argparse.ArgumentError:
            print('Ошибка в аргументах, попробуйте еще раз.\n')
            self.parser.print_help()
            exit()

class ImageLoader:
    """
    класс содержит утилиты для загрузки изображений из указанной папки
    путь переданный в конструктор должен быть корректным
    """

    def __init__(self, path_to_images):
        self._PATH_TO_IMAGES = path_to_images

    def resize_images(self, images, width, height) -> None:
        for i in range(len(images)):
            images[i] = images[i].resize( (width, height) )

    def get_images_with_names(self) -> tuple[list[str], list[Image]]:
        images = ([], [])
        image_names = os.listdir(self._PATH_TO_IMAGES)

        for image_name in image_names:
            path_to_image = f'{self._PATH_TO_IMAGES}{image_name}'
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
    
    def __init__(self, images, images_width, images_height, path_to_output_image = './output/'):
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
        count_pixels = image.width * image.width
        
        for width in range(image.width):
            for height in range(image.height):
                pixel = image.getpixel( (width, height) )
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
            distance = self._get_distance_between_pixels(pixel, self._avg_colors_images[i])
            
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
        print('\nГенерация мозаики начата')

        new_image_pixels = []
        new_image_width = old_image.width * self._images_width
        new_image_height = old_image.height * self._images_height

        for h in range(old_image.height):
            for w in range(old_image.width):
                pixel = old_image.getpixel( (w, h) )
                closest_image_ids = self._find_index_of_closest_by_avg_color_image(pixel)
                new_image_pixels.append(closest_image_ids)


        new_image = Image.new('RGB', (new_image_width, new_image_height))

        i = 0
        for h in range(old_image.height):
            for w in range(old_image.width):
                new_w = w * self._images_width
                new_h = h * self._images_height
                image_to_replace_pixel = self._images[new_image_pixels[i]]
                new_image.paste( image_to_replace_pixel, (new_w, new_h) )
                i += 1    
                    
        output_image_counter = 0
        output_image_name = f'{self._path_to_output_image}output_image_{output_image_counter}.jpg'
        while os.path.exists(output_image_name):
            output_image_counter += 1
            output_image_name = f'{self._path_to_output_image}output_image_{output_image_counter}.jpg'

        new_image.save(output_image_name)
        return output_image_name      


if __name__ == '__main__':
    argparser = CLIArgsParser()
    args = argparser.get_args() 
    print(args)
    exit()

    image_loader = ImageLoader(args['path_to_images'])
    images_with_names = image_loader.get_images_with_names()

    width = args['width_of_output_image']
    height = args['height_of_output_image']
    image_loader.resize_images(images_with_names[1], width, height)

    
    mosaic_generator = MosaicCreator(images_with_names[1], width, height)

    path_to_imagebase_for_mosaic = args['path_to_imagebase_for_mosaic']
    image = image_loader.get_image_by_path(path_to_imagebase_for_mosaic)

    path_to_output_image = mosaic_generator.create_and_show_mosaic_image(image)
    print(path_to_output_image)

    