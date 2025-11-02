from PIL import Image
import os

class UserInput:
    """
    Класс содержит утилиты для ввода и валидации данных от пользователя
    """

    def get_images_size(self) -> tuple[int, int]:
        """
        Запрашивает размер к которому будут приведены изображения, замещающие пиксели в мозаике.
        Соотношение сторон должно быть равно 1
        """
        print('Каждое изображение будет приведено к одинаковому размеру')
    
        width = 50
        height = 50

        if input(f'Если хотите изменить размер по умолчанию ({width}, {height}) введите любой символ (иначе нажмите Enter) ') != '':
            print('Не используйте слишком большой размер, соотношение сторон должно быть равно 1')
            width = int(input('Введите ширину в пикселях '))
            height = int(input('Введите высоту в пикселях '))
        
        if width != height:
            print('\nСоотношение сторон должно быть равно 1, попробуйте еще раз:')
            width, height = self.get_images_size()

        print(f'Все изображения будут приведены к размеру {width, height}', end='\n\n')
        
        return width, height

    def get_path_to_images(self) -> str:
        """
        Запрашивает у пользователя путь до папки с изображениями.
        Пытается прочитать список имен по указанному пути и открыть первое из списка как изображение.
        Если не удается, то вызывает самого себя пока не будет указан корректный путь.
        """

        message = """Введите путь до директории в формате ./(какой-то путь)/
        В указанной директории должны быть только изображения.
        """
        print(message)
        path_to_images_dir = input('Или нажмите Enter чтобы оставить ./images/ по умолчанию: ')
    
        if path_to_images_dir == '':
            path_to_images_dir = './images/'

        try:
            image_names = os.listdir(path_to_images_dir)
            for image_name in image_names:
                Image.open(f'{path_to_images_dir}{image_name}').close()
        except:
            error_message = '\nВведенный путь некорректен или в папке есть не поддерживаемые файлы, попробуйте заново:'
            print(error_message)
            path_to_images_dir = self.get_path_to_images() 

        return path_to_images_dir

    def get_path_to_imagebase_for_mosaic(self) -> str:
        """
        Запрашивает у пользователя путь до изображения, по которому строится мозаика
        Пытается открыть указанный файл как изображение. Если не удается, то вызывает
        самого себя пока не будет указан корректный путь.
        """
        message = """Необходимо указать путь до файла по которому будет строиться мозаика
Путь должен указываться в формате ./(какой-то путь до директории/название файла.расширение)
Конечный размер полученного изображения зависит от разрешения изображения по которому
строится мозаика. Использование исходного изображения со слишком большим разрешением вызовет
ошибку из-за недостатка памяти для работы программы"""
        print(message)
        
        path_to_imagebase = input('Введите путь до файла: ')

        try:
            Image.open(path_to_imagebase).close()
        except:
            print('\nВведенный путь некорректен или файл не поддерживается, попробуйте заново:')
            path_to_imagebase = self.get_path_to_imagebase_for_mosaic() 

        return path_to_imagebase
        
class ImageLoader:
    """
    класс содержит утилиты для загрузки изображений из указанной папки
    путь переданный в конструктор должен быть корректным
    """

    def __init__(self, path_to_images):
        self._PATH_TO_IMAGES = path_to_images

    def resize_images(self, images, width, height):
        width = 25
        height = 15
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

    def create_and_show_mosaic_image(self, old_image):
        """
        создает изображение new_image где пиксели в old_image заменены 
        на ближайшие по среднему цвету изображения из images
        возрвращает путь до него и показывает изображение
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
        new_image.show()
        return output_image_name      



if __name__ == '__main__':
    user_input = UserInput()
    path_to_images = user_input.get_path_to_images()
    image_loader = ImageLoader(path_to_images)
    print(f'Изображения берутся из директории {path_to_images}', end='\n\n')

    images_with_names = image_loader.get_images_with_names()
    
    images_size = user_input.get_images_size()
    width = images_size[0]
    height = images_size[1]

    image_loader.resize_images(images_with_names[1], width, height)

    path_to_imagebase_for_mosaic = user_input.get_path_to_imagebase_for_mosaic()

    mosaic_generator = MosaicCreator(images_with_names[1], width, height)

    image = image_loader.get_image_by_path(path_to_imagebase_for_mosaic)

    path_to_output_image = mosaic_generator.create_and_show_mosaic_image(image)
    print(path_to_output_image)

    