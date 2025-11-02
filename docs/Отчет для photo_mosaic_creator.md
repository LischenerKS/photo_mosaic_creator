# Отчет по работе приложения
При запуске через консоль main.py выполняется [блок кода](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L137) 

Сначала [запускается classmetod get_images_with_names](    images_with_names = ImageLoader.get_images_with_names()) который возвращает список из списков вида [имя файла, объект Image из этого файла] 

[Далее просим у пользователя](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L141) название файла из которого он хочет сделать мозаику
[Проверяем путь к файлу ](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L143-L144)

[создаем список](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L146) images в котором будут только объекты Image из images_with_names 

Создаем объект класса MosaicCreator:
[обрабатываем список images в resize_images ](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L10-L14) Там фотографии которые мы будем использовать вместо пикселей уменьшаются, чтобы полученное фото не вышло слишком огромным (оно все равно выйдет огромным)
и передаем список, который вернул нам этот метод в конструктор MosaicCreator

[Вызывается init ](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L34-L43)
там инициализируются поля.
Для одного из полей [вызывается](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L65-L72) get_avg_colors_array (он возвращает список средних цветов из списка self.image )
Для получения среднего цвета списка внутри этого метода вызывается [get_avg_color_image](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L45-L63)
В нем для получения среднего цвета просто просматриваем все пиксели изображения и плюсуем значение соответствуещего цвета (r, g, b), после чего делим каждое из трех полученных значений на количество пикселей в изображении

[Вызывается ](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L149)
[i[1] for i in images_with_names if i[0] == image_to_mosaic][0]  тут мы отбираем из images_with_names путь к файлу, по которому пользователь хочет построить мозаику и так как это список из одного элемента берем нулевой (нам нужен не список с Image, а объект Image)
Для полученного объекта вызываем mosaic_generator.create_and_show_mosaic_image()

Этот метод должен построить новое изображение мозаики, сохранить его, показать и вернуть до него путь

[Сначала в нем для каждого пикселя старого изображения с помощью метода find_index_of_closest_by_avg_color_image() находим наиболее близкое по среднему цвету изображение](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L104-L112)

Метод find_index_of_closest_by_avg_color_image(pixel) работает просто проходится по списку средних цветов изображений и возвращает индекс ближайшего (индексы в этом списке совпадают со списком image, он так специально создан методом get_avg_colors_array еще в конструкторе)

Расстояние между цветами считается [методом](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L74-L78) как сумма модулей разностей соответствующих цветов

[Наиболее близкие для каждого пикселя изображения найдены и осталось построить новое изображение](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L115-L124)
Для каждого пикселя на новое изображение добавляем наиболее близкую ему картинку (изображение будет больше в высоту и в ширину в колличество пикселей вставляемых изображений)

[Делаем незанятое имя для нового файла](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L126-L129)

[Сохраняем, показываем, возвращаем путь](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L126-L129)

[Значение возвращается в print, выполнение завершено](https://github.com/LischenerKS/photo_mosaic_creator/blob/8581b8bca2b040828be997d368367c0505aa8ec8/main.py#L149)