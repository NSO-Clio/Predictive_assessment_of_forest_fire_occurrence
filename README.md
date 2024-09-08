# Предиктивная оценка возникновения лесных пожаров

# О проекте
Наша команда разработала сегментационную модель машинного обучения, способную по снимкам со спутников указанной территории и метеорологическим данным возвращать маску потенциальных пожаров в ближайший месяц.

# Заказчик

<img style="width: 50%; height: auto;" src='https://github.com/user-attachments/assets/0454e9ab-5d6f-4643-ad78-e9a38fafe296'>

Минприроды, сделано в рамках хакатона Цифровой Прорыв сезон: Искусственный Интеллект

# Преимущества продукта:
* коэффициент корреляции Мэтьюса (MCC) >= 0.5 на тестовом датасете кейсодержателя
* реализован веб интерфейс
* простой в использовании программный модуль

# Структура проекта

- ```pipelines``` - папка в которой хранится анализ данных, а также скрипт преобразования файлов для обучение модели
- ```submit``` - ноутбук того как мы делали сабмит на тестовую выборку
- ```model``` - папка нашей библиотеки с моделью и ее весами
- ```sample``` - примеры того что должна получать на вход модель из нашей библилтеки
- ```branch/web-app``` - ветка с веб-интерфейсом [сслфка для удобного перехода](https://github.com/NSO-Clio/Predictive_assessment_of_forest_fire_occurrence/tree/web-app)
- ```web-app``` - папка в которой расположен веб интерфейс

# Стэк технологий

* numpy
* pandas
* scipy
* rasterio
* catboost
* opencv

# Архитектура

![image](https://github.com/user-attachments/assets/d4409661-aaf9-412a-b6ba-2ca6da6680a6)
 
# Работа с библиотекой

- Для начала нужно склонировать проект с Github'a:

```sh
git clone --no-checkout https://github.com/NSO-Clio/Predictive_assessment_of_forest_fire_occurrence
cd Predictive_assessment_of_forest_fire_occurrence
```

- И из репозитория взять папку ```model```, которая является библиотекей, после чего расположить ее в своем проекте

- После нужно установить requirements:

```sh
pip install -r requirements.txt
```

- Пример кода использоавания

```py
from model import CatNet


model = CatNet()

preproc_img = model.preproc(image_path='path/to/img.tiff', weather_data_path='path/to/weather_img.csv') # Получен преобразоаваное фото со спутника в датафрейм, а так же размер изображения для дальнейшего развертывания

predict = model.predict_segment(*preproc_img)

model.predict_segment(*preproc_img, save_path='save/path/mask.jpg')
```

- Пример какие файлы нужно подавать в модель вы увидите в папке [sample](sample/)

# Запуск веб интерфейса

```sh
pip install -r requirements.txt

python web-app/app.py
```

после чего в консоли у вас появится ссылка

# Команда 
* [Сусляков Семён](https://github.com/ssuslyakoff)
* [Андреасян Егор](https://github.com/EgorAndrik)
* [Вершинин Михаил](https://github.com/Rasdafar128)
* [Ротачёв Александр](https://github.com/Sasha2810)
