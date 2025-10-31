from PIL import Image
import os

class ImageLoader:
    #*класс содержит утилиты для загрузки изображений из указанной папки

    def _get_path_to_images(self) -> str:
        path_to_images = input('Введите путь до директории с изображениями в формате или нажмите Enter чтобы оставить ./images/ по умолчанию: ')
    
        if path_to_images == '':
            path_to_images = './images/'

        print(f'Изображения берутся из директории {path_to_images}', end='\n\n')
        return path_to_images

    def get_images_size(self) -> tuple[int, int]:
        print('Каждое изображение будет приведено к одинаковому размеру')
    
        width = 25
        height = 25

        if input(f'Если хотите изменить размер по умолчанию ({width}, {height}) введите любой символ (иначе нажмите Enter) ') != '':
            print('Не используйте слишком большой размер')
            width = int(input('Введите ширину в пикселях '))
            height = int(input('Введите высоту в пикселях '))

        print(f'Все изображения будут приведены к размеру {width, height}', end='\n\n')
        
        return width, height

    def __init__(self):
        self._PATH_TO_IMAGES = self._get_path_to_images()

    def resize_images(self, images, width, height):
        for i in range(len(images)):
            images[i] = images[i].resize( (width, height) )

    def get_images_with_names(self) -> list[list[str], list[Image]]:
        images = [[], []]
        image_names = os.listdir(self._PATH_TO_IMAGES)

        for image_name in image_names:
            path_to_image = f'{self._PATH_TO_IMAGES}{image_name}'

            with Image.open(path_to_image) as img:
                img.load()
                images[0].append(image_name)
                images[1].append(img)

        return images

    def get_image_by_name(self, name) -> Image:
        path = f'{self._PATH_TO_IMAGES}{name}'
        
        with Image.open(path) as img:
            img.load()
            image = img

        return image

class MosaicCreator:
    #*класс для генерации мозаики
    
    def __init__(self, images, images_width, images_height, path_to_output_image = './output/'):
        self._images = images 
        self._avg_colors_images = self._get_avg_colors_array()

        self._path_to_output_image = path_to_output_image

        self._images_width = images_width
        self._images_height = images_height

        self._output_image_counter = 0

    def _get_avg_color_image(self, image) -> tuple[int, int, int]:
        #метод возвращающий для изображения его средний цвет 
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

        return (r, g, b)

    def _get_avg_colors_array(self) -> list[tuple[int, int, int]]:
        #метод возвращающий для self.images массив средних цветов 
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
        #находит в self.avg_colors_images ближайшее по среднему цвету изображение
        #к переданному pixel и возвращает его index

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
        #создает изображение new_image где пиксели в old_image заменены 
        #на ближайшие по среднему цвету изображения из images
        #возрвращает путь до него и показывает изображение

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

        output_image_name = f'{self._path_to_output_image}output_image_{self._output_image_counter}.jpg'
        while os.path.exists(output_image_name):
            self._output_image_counter += 1
            output_image_name = f'{self._path_to_output_image}output_image_{self._output_image_counter}.jpg'

        new_image.save(output_image_name)
        new_image.show()
        return output_image_name      



if __name__ == '__main__':
    image_loader = ImageLoader()
    
    images_with_names = image_loader.get_images_with_names()
    
    images_size = image_loader.get_images_size()
    width = images_size[0]
    height = images_size[1]

    image_loader.resize_images(images_with_names[1], width, height)

    image_to_mosaic_name = input('Введите название файла из указанной директории по которому будет строиться мозаика: ')

    mosaic_generator = MosaicCreator(images_with_names[1], width, height)

    image = image_loader.get_image_by_name(image_to_mosaic_name)

    path_to_output_image = mosaic_generator.create_and_show_mosaic_image(image)
    print(path_to_output_image)

    